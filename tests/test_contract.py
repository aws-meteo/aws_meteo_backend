import sys
from unittest.mock import MagicMock, patch

import numpy as np
import pandas as pd
import xarray as xr
from fastapi.testclient import TestClient

# Mock s3_helpers BEFORE importing app to avoid S3 dependency
mock_s3 = MagicMock()
mock_s3.list_runs.return_value = ["2025010100"]
mock_s3.list_steps.return_value = ["000"]
mock_s3.load_dataset.return_value = MagicMock()
sys.modules["app.s3_helpers"] = mock_s3

from app.main import app

client = TestClient(app)


def _build_test_dataset() -> xr.Dataset:
    times = pd.date_range("2020-01-01", periods=2, freq="MS")
    lats = np.array([40.0, 41.0])
    lons = np.array([-4.0, -3.0])
    data = np.array(
        [
            [[280.0, 281.0], [282.0, 283.0]],
            [[284.0, 285.0], [286.0, 287.0]],
        ],
        dtype=float,
    )

    return xr.Dataset(
        {"t2m": (["valid_time", "latitude", "longitude"], data)},
        coords={"valid_time": times, "latitude": lats, "longitude": lons},
    )


def test_historic_t2m_contract():
    payload = {
        "points": [
            {"lat": 40.4168, "lon": -3.7038},
        ]
    }

    with patch(
        "app.lib.historic.extract.load_merged_dataset",
        return_value=_build_test_dataset(),
    ):
        response = client.post("/historic/t2m", json=payload)

    assert response.status_code == 200
    body = response.json()

    assert "data" in body
    assert isinstance(body["data"], list)
    assert body["data"]
    assert "series" in body["data"][0]
    assert body["data"][0]["series"]

    first_item = body["data"][0]["series"][0]
    assert "date" in first_item
    assert "value" in first_item
    assert "timestamp" in first_item
