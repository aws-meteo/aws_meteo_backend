from __future__ import annotations

import os
import re
import logging
import threading
import tempfile
import uuid
from typing import List, Set, Any

import xarray as xr
from cachetools import cached, TTLCache
from filelock import FileLock

from ..config import settings
from ..integrations.s3 import get_s3_client, get_s3_fs

logger = logging.getLogger(__name__)

# Configuración básica de STI
BUCKET = settings.S3_BUCKET_NAME
BASE_PREFIX = "indices/sti/"
INDEX_NAME = "sti"
REGION_NAME = "chile"

# Metadata Cache (TTL 5 mins)
METADATA_CACHE = TTLCache(maxsize=128, ttl=300)

# Global lock para HDF5 (Library-level safety)
_HDF5_LOCK = threading.Lock()

# Clientes (usando integraciones)
s3_client = get_s3_client()
s3_fs = get_s3_fs()


def _normalize_step(step: str | int) -> str:
    """
    Normaliza el step a 3 dígitos (e.g. 48 -> '048').
    """
    return f"{int(step):03d}"


def _object_exists(key: str) -> bool:
    """
    Verifica existencia de un objeto en S3 usando s3fs.
    """
    path = f"{BUCKET}/{key}"
    try:
        return s3_fs.exists(path)
    except Exception as exc:
        logger.error("Error verificando existencia en S3 para %s: %s", path, exc)
        return False


@cached(METADATA_CACHE)
def list_runs() -> List[str]:
    """
    Lista los 'run=YYYYMMDDHH' leyendo las sub-carpetas (CommonPrefixes).
    """
    paginator = s3_client.get_paginator("list_objects_v2")
    runs: Set[str] = set()

    for page in paginator.paginate(Bucket=BUCKET, Prefix=BASE_PREFIX, Delimiter="/"):
        for prefix_info in page.get("CommonPrefixes", []):
            prefix = prefix_info.get("Prefix")
            m = re.search(r"run=(\d{10})/?", prefix)
            if m:
                runs.add(m.group(1))

    return sorted(runs)


@cached(METADATA_CACHE)
def list_steps(run: str) -> List[str]:
    """
    Lista los 'step=XXX' leyendo las sub-carpetas (CommonPrefixes) dentro de un run.
    """
    prefix_path = f"{BASE_PREFIX}run={run}/"
    paginator = s3_client.get_paginator("list_objects_v2")
    steps: Set[str] = set()

    for page in paginator.paginate(Bucket=BUCKET, Prefix=prefix_path, Delimiter="/"):
        for prefix_info in page.get("CommonPrefixes", []):
            prefix = prefix_info.get("Prefix")
            m = re.search(r"step=(\d{3})/?", prefix)
            if m:
                steps.add(m.group(1))

    return sorted(steps)


def build_nc_key(run: str, step: str | int) -> str:
    """
    Construye el key del NetCDF según la convención en S3.
    """
    step_str = _normalize_step(step)
    filename = f"{INDEX_NAME}_{REGION_NAME}_run={run}_step={step_str}.nc"
    key = f"{BASE_PREFIX}run={run}/step={step_str}/{filename}"
    return key


def build_nc_s3_uri(run: str, step: str | int) -> str:
    """
    Construye la URI tipo 's3://bucket/...' para uso informativo.
    """
    key = build_nc_key(run, step)
    return f"s3://{BUCKET}/{key}"


def pick_data_var(ds: xr.Dataset, preferred: str = "sti") -> str:
    """
    Selecciona la variable de datos correcta del dataset.
    """
    if preferred in ds.data_vars:
        return preferred

    if "var" in ds.data_vars:
        return "var"

    if len(ds.data_vars) == 1:
        found = str(next(iter(ds.data_vars)))
        logger.warning(f"Variable preferida '{preferred}' no encontrada. Usando única variable: '{found}'")
        return found

    raise KeyError(f"Variable '{preferred}' no encontrada y no se pudo deducir una única variable. Disponibles: {list(ds.data_vars)}")


def load_dataset(run: str, step: str | int) -> xr.Dataset:
    """
    Descarga robusta y thread-safe de NetCDF desde S3 y lo carga en memoria.
    """
    key = build_nc_key(run, step)
    step_str = _normalize_step(step)
    local_filename = f"sti_{run}_{step_str}.nc"
    temp_dir = tempfile.gettempdir()
    final_path = os.path.join(temp_dir, local_filename)
    lock_path = final_path + ".lock"

    lock = FileLock(lock_path, timeout=60)

    with lock:
        if os.path.exists(final_path):
            try:
                with _HDF5_LOCK:
                    with xr.open_dataset(final_path, engine="h5netcdf", cache=False) as ds_check:
                        pass
                logger.info(f"Cache HIT y fichero válido: {final_path}")
            except Exception as e:
                logger.warning(f"Cache corrupto detectado en {final_path} ({e}). Borrando para re-descargar.")
                try:
                    os.remove(final_path)
                except OSError:
                    pass

        if not os.path.exists(final_path):
            tmp_download_path = os.path.join(temp_dir, f"{local_filename}.{uuid.uuid4()}.tmp")
            logger.info(f"Iniciando descarga: {key} -> {tmp_download_path}")
            try:
                s3_client.download_file(BUCKET, key, tmp_download_path)

                if os.path.getsize(tmp_download_path) < 100:
                    raise ValueError("El archivo descargado es demasiado pequeño (<100B).")

                with _HDF5_LOCK:
                    with xr.open_dataset(tmp_download_path, engine="h5netcdf", cache=False) as ds_test:
                        pass

                os.replace(tmp_download_path, final_path)
                logger.info(f"Descarga validada y publicada en: {final_path}")

            except Exception as e:
                logger.error(f"Fallo en descarga/validación de {key}: {e}")
                if os.path.exists(tmp_download_path):
                    try:
                        os.remove(tmp_download_path)
                    except:
                        pass
                raise

    try:
        with _HDF5_LOCK:
            logger.info(f"Opening dataset {final_path} with h5netcdf")
            ds = xr.open_dataset(final_path, engine="h5netcdf", cache=False)

            target_var = pick_data_var(ds, preferred="sti")
            if target_var != "sti":
                logger.info(f"Renombrando variable '{target_var}' -> 'sti'")
                ds = ds.rename({target_var: "sti"})

            logger.info(f"Starting eager load for {final_path}")
            ds.load()
            logger.info(f"Finished eager load for {final_path}")

        return ds

    except Exception as e:
        logger.error(f"Error fatal abriendo/cargando dataset {final_path}: {e}")
        raise
