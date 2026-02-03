import pytest
from unittest.mock import MagicMock, patch
import app.s3_helpers as s3_helpers

@pytest.fixture
def mock_s3_client():
    """Mocks the s3_client in s3_helpers module."""
    with patch.object(s3_helpers, 's3_client') as mock:
        yield mock

@pytest.fixture(autouse=True)
def clear_cache():
    """Clears the metadata cache before and after each test to prevent test pollution."""
    s3_helpers.METADATA_CACHE.clear()
    yield
    s3_helpers.METADATA_CACHE.clear()

@pytest.mark.timeout(5)
def test_list_runs_caching(mock_s3_client):
    """
    Test that list_runs uses caching.
    
    Scenario:
    1. Setup mock to return a standard structure.
    2. Call list_runs() twice.
    3. Assert s3_client.get_paginator or underlying method is called exactly ONCE.
    """
    # Setup mock behavior
    mock_paginator = MagicMock()
    mock_s3_client.get_paginator.return_value = mock_paginator
    
    # Mock pagination return - just one page with one prefix
    mock_paginator.paginate.return_value = [{
        "CommonPrefixes": [{"Prefix": "indices/sti/run=2025010100/"}]
    }]
    
    # 1. First Call
    runs1 = s3_helpers.list_runs()
    assert "2025010100" in runs1
    
    # 2. Second Call (Should hit cache if implemented)
    runs2 = s3_helpers.list_runs()
    assert "2025010100" in runs2
    
    # 3. Assertions
    # We expect get_paginator to be called only ONCE if caching is working.
    # Currently (RED phase), it should be called TWICE.
    # The test allows us to verify the current state (failure expected).
    
    # STRICT CHECK: We want to fail if it's called more than once
    # But for TDD "RED", we write the test asserting the DESIRED behavior (once).
    # It will fail now, which is correct.
    assert mock_s3_client.get_paginator.call_count == 1, \
        f"Expected 1 call to S3, but got {mock_s3_client.get_paginator.call_count}"

@pytest.mark.timeout(5)
def test_list_steps_caching(mock_s3_client):
    """
    Test that list_steps uses caching.
    """
    s3_helpers.METADATA_CACHE.clear()
    
    # Setup mock
    mock_paginator = MagicMock()
    mock_s3_client.get_paginator.return_value = mock_paginator
    
    # Explicitly print what we are setting
    prefix_mock = "indices/sti/run=2025010100/step=001/"
    print(f"\nDEBUG: Setting mock prefix to {prefix_mock}")
    
    mock_paginator.paginate.return_value = [{
        "CommonPrefixes": [{"Prefix": prefix_mock}]
    }]
    
    # Calls
    print("DEBUG: Calling list_steps first time")
    steps1 = s3_helpers.list_steps("2025010100")
    print(f"DEBUG: steps1 result: {steps1}")
    
    print("DEBUG: Calling list_steps second time")
    steps2 = s3_helpers.list_steps("2025010100")
    print(f"DEBUG: steps2 result: {steps2}")
    
    if "001" not in steps1:
        print(f"DEBUG: FAILURE! '001' not in {steps1}")
        # List what WAS generated
        print(f"DEBUG: Mock calls: {mock_s3_client.mock_calls}")

    
    assert "001" in steps1
    assert steps1 == steps2
    
    # Assert single call
    assert mock_s3_client.get_paginator.call_count == 1, \
        f"Expected 1 call to S3, but got {mock_s3_client.get_paginator.call_count}"
