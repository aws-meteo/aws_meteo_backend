# Local Development Environment & S3 Access

This document explains how to set up and verify the local development environment, specifically regarding S3 access for the modular architecture.

## Modular Architecture Overview

The backend is organized into three main layers for STI (Standardized Terrestrial Index) data:

1.  **Integrations (`app/integrations/s3.py`)**: Factory functions for AWS clients.
    - `get_s3_client()`: Returns a `boto3` S3 client.
    - `get_s3_fs()`: Returns an `fsspec` S3 filesystem.
2.  **Services (`app/services/sti_service.py`)**: Business logic and data access.
    - Handles S3 object listing (`run=...`, `step=...`).
    - Robust, thread-safe NetCDF loading from S3 with local caching in `/tmp`.
    - Uses `h5netcdf` as the backend engine for `xarray`.
3.  **Routers (`app/routers/sti.py`)**: FastAPI endpoints.
    - Exposes API for listing runs, steps, and retrieving data summaries/subsets.

## S3 Connectivity Verification

To ensure your environment is correctly configured to reach the data bucket, use the following script:

```bash
python scripts/verify_s3_connectivity.py
```

This script will:
- Validate your AWS credentials.
- Report the current identity (IAM user/role).
- Attempt to list folders in the `indices/sti/` prefix of the configured bucket.

## Running the Backend Locally with S3 Access

To run the containerized backend locally while allowing it to access S3 using your local AWS credentials, use the provided helper script:

```bash
./scripts/run_local_s3.sh [profile_name]
```

### How it works:
- **Volume Mounting**: It mounts your local `~/.aws` directory to `/root/.aws` inside the container in read-only mode (`-v "$HOME/.aws:/root/.aws:ro"`).
- **Environment Variables**: It passes `AWS_PROFILE`, `AWS_REGION`, and `S3_BUCKET_NAME` to the container.
- **Pass-through Logic**: By setting `AWS_PROFILE`, the `boto3` client inside the container will look for the corresponding credentials in the mounted volume.

**Note**: Ensure your local user has the necessary IAM permissions to list and get objects from the target S3 bucket.

## Dependencies

- **`h5netcdf`**: This library is now a required dependency for loading NetCDF files. It is used as the engine in `xarray.open_dataset` for better performance and compatibility with HDF5-based NetCDF4 files in the container environment.
