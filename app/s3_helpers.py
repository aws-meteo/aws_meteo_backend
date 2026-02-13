"""
DEPRECATED: This module is being split. 
Please use app.services.sti_service for STI logic 
and app.integrations.s3 for S3 client factories.
"""
from .services.sti_service import (
    list_runs,
    list_steps,
    load_dataset,
    build_nc_key,
    build_nc_s3_uri,
    METADATA_CACHE,
    s3_client,
    s3_fs,
    _normalize_step,
    _object_exists,
    pick_data_var,
    BUCKET,
    BASE_PREFIX,
    INDEX_NAME,
    REGION_NAME,
    _HDF5_LOCK
)

