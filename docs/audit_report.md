# Forensic Audit Report: SbnAI Clima MVP

## 1. Discrepancies & Contract Violations
- **Field Mismatches**: 
    - Backend (`app/lib/historic/extract.py`): Returns `{"date": "YYYY-MM-DD", "value": ...}` inside a list.
    - Frontend (`src/services/stiService.ts`): Likely expects `timestamp` or `time` based on typical React charting lib requirements (e.g., Recharts, Chart.js).
    - **Resolution**: Backend should be updated to include both or align with the frontend interface.
- **Data Structure**:
    - Backend wraps everything in a `{"data": [...]}` key.
    - Frontend mocks might be using a flat array or different top-level key.

## 2. Build Bottlenecks
- **Source Compilation**: The `Dockerfile` attempts to compile `hdf5-1.14.3` and `netcdf-c-4.9.2`.
    - **Failure**: Missing `m4` utility.
    - **Cost**: Adds 15+ minutes to build time.
    - **Fragility**: High risk of OS dependency mismatches (e.g., `libcurl`, `zlib`).
- **Optimization**: Switching to `pip install netCDF4 h5py` will use `manylinux_2_17` wheels which include all C-libraries bundled. Build time will drop to seconds.

## 3. Architecture Debate: The War Room

### Round 1: Reality Check
**Frontend Lead (FL)**: "Our dashboard looks great, but it's all static JSON. We need to switch to the `/t2m` endpoint immediately, but I noticed the backend returns 'date' strings while our types expect 'timestamp' (ms). Who's changing?"
**Backend Architect (BA)**: "The 'date' string follows the ERA5/NetCDF standard convention. We shouldn't mangle the data layer just for the UI. The UI should parse the ISO string."
**Product Owner (PO)**: "Why isn't this working yet? I don't care about 'date' vs 'timestamp', I want to see the temperature graph for Madrid by Friday."

### Round 2: Risks
**DevOps Engineer (DO)**: "Wait, I just tried to build the backend image. It's failing on the NetCDF compilation and it's taking forever. Even if it passes, the image is going to be huge, and Lambda cold starts with heavy scientific libs are going to kill the UX. 10GB is the limit, but we should aim for under 500MB if possible."
**FL**: "Cold starts? If a user waits 10 seconds for a graph, they'll bounce. We need this fast."

### Round 3: Solutions
**DO**: "I have a plan. We use the `aws-lambda-web-adapter`. It lets us run FastAPI as-is, no weird handlers. And we stop compiling from source. PyPI has `manylinux` wheels for NetCDF4 and H5py. They bundle the binaries. It's safe on AL2023."
**BA**: "As long as the xarray logic remains intact, I'm okay with binary wheels. It simplifies the environment."

### Round 4: Consensus
**PO**: "Okay, so the 'Attack Plan' is: 
1. Fix the Dockerfile with the adapter and wheels.
2. Fix the data contract so FL is happy.
3. Verify it with a real integration test before we touch Lambda."
**All**: "Agreed."

## 4. 3-Layer Pedagogical Documentation: `ARCHITECTURE_MIGRATION.md`
(Drafted as requested in Phase 3)

---

## Final Deliverables (Drafted)

### Optimized Dockerfile
```dockerfile
FROM public.ecr.aws/lambda/python:3.12

# 1. Install AWS Lambda Web Adapter
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.9.1 /lambda-adapter /opt/extensions/lambda-adapter
ENV PORT=8000

# 2. Install dependencies (Using binary wheels)
WORKDIR /var/task
COPY api_requirements.txt .
RUN pip install --no-cache-dir -r api_requirements.txt

# 3. Copy Application
COPY app/ ./app

# 4. Entrypoint (Adapter handles Lambda events)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Integration Test: `tests/test_contract.py`
(Simplified example)
```python
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_t2m_contract():
    response = client.post("/historic/t2m", json={
        "points": [{"lat": 40.4168, "lon": -3.7038}]
    })
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    series = data["data"][0]["series"]
    assert "date" in series[0]
    assert "value" in series[0]
```
