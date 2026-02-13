import os
import pytest
import xarray as xr
import numpy as np
import boto3
from moto import mock_aws
from unittest.mock import patch
import tempfile
from typing import Any
from pathlib import Path

# We import the service here
from app.services import sti_service
from app.config import settings

@pytest.fixture(scope="function")
def aws_credentials() -> None:
    os.environ["AWS_ACCESS_KEY_ID"] = "testing"
    os.environ["AWS_SECRET_ACCESS_KEY"] = "testing"
    os.environ["AWS_SECURITY_TOKEN"] = "testing"
    os.environ["AWS_SESSION_TOKEN"] = "testing"
    os.environ["AWS_DEFAULT_REGION"] = "us-east-1"

@pytest.fixture(scope="function")
def mocked_s3(aws_credentials: Any) -> Any:
    with mock_aws():
        conn = boto3.client("s3", region_name="us-east-1")
        conn.create_bucket(Bucket=settings.S3_BUCKET_NAME)
        yield conn

@pytest.fixture(scope="function")
def clean_temp_dir() -> Any:
    yield
    # Cleanup artifacts in system temp directory to prevent test cross-contamination
    temp_dir = tempfile.gettempdir()
    for f in os.listdir(temp_dir):
        if f.startswith("sti_") and (f.endswith(".nc") or f.endswith(".lock") or ".tmp" in f):
            try:
                os.remove(os.path.join(temp_dir, f))
            except:
                pass

def test_list_runs(mocked_s3: Any) -> None:
    bucket_name = settings.S3_BUCKET_NAME
    runs = ["2024021300", "2024021312"]
    for run in runs:
        # Simulate S3 directory structure via CommonPrefixes
        mocked_s3.put_object(Bucket=bucket_name, Key=f"indices/sti/run={run}/dummy.txt")
    
    sti_service.METADATA_CACHE.clear()
    
    with patch("app.services.sti_service.s3_client", mocked_s3):
        result = sti_service.list_runs()
        assert result == sorted(runs)

def test_list_steps(mocked_s3: Any) -> None:
    bucket_name = settings.S3_BUCKET_NAME
    run = "2024021300"
    steps = ["000", "024", "048"]
    for step in steps:
        mocked_s3.put_object(Bucket=bucket_name, Key=f"indices/sti/run={run}/step={step}/dummy.txt")
    
    sti_service.METADATA_CACHE.clear()
    
    with patch("app.services.sti_service.s3_client", mocked_s3):
        result = sti_service.list_steps(run)
        assert result == sorted(steps)

def test_load_dataset_moto(mocked_s3: Any, tmp_path: Path, clean_temp_dir: Any) -> None:
    bucket_name = settings.S3_BUCKET_NAME
    run = "2024021300"
    step = "024"
    step_str = "024"
    filename = f"sti_chile_run={run}_step={step_str}.nc"
    key = f"indices/sti/run={run}/step={step_str}/{filename}"
    
    # Generate minimal NetCDF for meteorological data simulation
    data = np.random.rand(10, 10).astype(np.float32)
    ds = xr.Dataset(
        {"sti": (("y", "x"), data)},
        coords={"y": np.arange(10), "x": np.arange(10)}
    )
    
    local_file = tmp_path / "test.nc"
    ds.to_netcdf(str(local_file), engine="h5netcdf")
    mocked_s3.upload_file(str(local_file), bucket_name, key)
    
    target_local_path = os.path.join(tempfile.gettempdir(), f"sti_{run}_{step_str}.nc")
    if os.path.exists(target_local_path):
        os.remove(target_local_path)
    
    with patch("app.services.sti_service.s3_client", mocked_s3):
        loaded_ds = sti_service.load_dataset(run, step)
        
        assert "sti" in loaded_ds.data_vars
        assert loaded_ds.sti.shape == (10, 10)
        xr.testing.assert_allclose(ds, loaded_ds)
        # Verify eager load into memory
        assert loaded_ds.sti.values is not None

def test_load_dataset_with_alternative_var_name(mocked_s3: Any, tmp_path: Path, clean_temp_dir: Any) -> None:
    bucket_name = settings.S3_BUCKET_NAME
    run = "2024021312"
    step = 48
    step_str = "048"
    filename = f"sti_chile_run={run}_step={step_str}.nc"
    key = f"indices/sti/run={run}/step={step_str}/{filename}"
    
    ds = xr.Dataset(
        {"var": (("y", "x"), np.random.rand(5, 5).astype(np.float32))},
        coords={"y": np.arange(5), "x": np.arange(5)}
    )
    
    local_file = tmp_path / "test_var.nc"
    ds.to_netcdf(str(local_file), engine="h5netcdf")
    mocked_s3.upload_file(str(local_file), bucket_name, key)
    
    with patch("app.services.sti_service.s3_client", mocked_s3):
        loaded_ds = sti_service.load_dataset(run, step)
        # Verify variable renaming logic
        assert "sti" in loaded_ds.data_vars
        assert "var" not in loaded_ds.data_vars
