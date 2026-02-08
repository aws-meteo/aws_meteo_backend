# SbnAI Clima: Architecture Migration (MVP)

This document outlines the transition from the current development state to the MVP target architecture for the AWS Lambda-based backend.

| Layer | Current State (Broken/Mocked) | Target State (MVP) |
| :--- | :--- | :--- |
| **User Layer** | Frontend displays random mock data for temperature graphs. | Frontend displays real ERA5 historical data (t2m). |
| **Logic Layer** | Backend requires complex source compilation; Custom Lambda handlers. | AWS Lambda Web Adapter runs standard FastAPI; Binary wheels for scientific libs. |
| **Data Layer** | Local NetCDF files or missing data links. | S3-hosted NetCDF/Zarr accessed via Xarray/fsspec. |

### Key Improvements
- **Docker Optimization**: Removed HDF5/NetCDF-C source compilation. Switched to PyPI binary wheels, reducing build time from 15 mins to < 1 min.
- **Data Contract**: Added `timestamp` (Unix epoch milliseconds) to the backend response series to ensure direct compatibility with frontend charting libraries.
- **Portability**: Added `.devcontainer` configuration to replicate the production environment locally on port 8000.
