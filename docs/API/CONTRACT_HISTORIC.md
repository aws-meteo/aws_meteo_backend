# API Contract: Historic Temperature (T2M)

## Endpoint
`POST /historic/t2m`

## Description
Retrieves historical monthly temperature series for a list of geographic points.

## Request Format (JSON)
| Field | Type | Description | Required |
| :--- | :--- | :--- | :--- |
| `points` | List[Object] | List of geographic points with `lat` and `lon`. | Yes |
| `units` | String | Target temperature units: `"C"` (Celsius) or `"K"` (Kelvin). Defaults to `"C"`. | No |

### Sample Request
```json
{
  "points": [
    { "lat": 40.4168, "lon": -3.7038 }
  ],
  "units": "C"
}
```

## Response Format (JSON)
The response contains a `data` array, where each element corresponds to a requested point.

| Field | Type | Description |
| :--- | :--- | :--- |
| `lat_requested` | Float | The latitude provided in the request. |
| `lon_requested` | Float | The longitude provided in the request. |
| `lat_used` | Float | The actual latitude of the nearest grid point used. |
| `lon_used` | Float | The actual longitude of the nearest grid point used. |
| `variable` | String | The meteorological variable (e.g., `"t2m"`). |
| `units` | String | The units of the returned values. |
| `series` | List[Object] | The time series data. |

### Series Item Format
| Field | Type | Description |
| :--- | :--- | :--- |
| `date` | String | ISO date string (`YYYY-MM-DD`). |
| `timestamp` | Integer | Unix epoch milliseconds (for frontend charting). |
| `value` | Float | The temperature value. |

### Sample Response
```json
{
  "data": [
    {
      "lat_requested": 40.4168,
      "lon_requested": -3.7038,
      "lat_used": 40.5,
      "lon_used": -3.75,
      "variable": "t2m",
      "units": "C",
      "series": [
        {
          "date": "2020-01-01",
          "timestamp": 1577836800000,
          "value": 8.5
        }
      ]
    }
  ]
}
```
