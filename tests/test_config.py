import os
import pytest
from pydantic import ValidationError

# We will import the Settings class. 
# Since app.config might not exist yet during the first run of this test logic if we were strictly following "fail first" 
# but we need the class definition to fail on it. 
# However, standard TDD implies writing the test that USES the code.
# Attempting to import it will fail if it doesn't exist, which counts as "red".

try:
    from app.config import Settings
except ImportError:
    Settings = None

def test_settings_load_env_vars(monkeypatch):
    """Test that settings load correctly from environment variables."""
    if Settings is None:
        pytest.fail("Could not import Settings from app.config")

    monkeypatch.setenv("S3_BUCKET_NAME", "test-bucket")
    monkeypatch.setenv("AWS_REGION", "us-east-1")
    monkeypatch.setenv("CORS_ORIGINS", "http://localhost:3000,https://myapp.com")

    settings = Settings()

    assert settings.S3_BUCKET_NAME == "test-bucket"
    assert settings.AWS_REGION == "us-east-1"
    assert settings.CORS_ORIGINS == ["http://localhost:3000", "https://myapp.com"]

def test_settings_defaults(monkeypatch):
    """Test defaults if they are set (or fail if fields are required)."""
    if Settings is None:
        pytest.fail("Could not import Settings from app.config")
        
    # Unset critical vars to see if it uses defaults or raises error
    # For this exercise, we want to ensure we HAVE some defaults or specific behavior
    # strictly based on the user prompt: "valores por defecto seguros"
    
    # Let's assume we want defaults for development if nothing is passed, 
    # OR we encourage explictness. 
    # User prompt said: "variables de entorno con valores por defecto seguros"
    
    # We clear env vars to test defaults
    monkeypatch.delenv("S3_BUCKET_NAME", raising=False)
    monkeypatch.delenv("AWS_REGION", raising=False)
    monkeypatch.delenv("CORS_ORIGINS", raising=False)
    
    settings = Settings()
    
    # Asserting expected defaults (these should match what we implement in config.py)
    # Based on current code:
    # BUCKET = "pangu-mvp-data"
    # REGION = "chile" (actually it was REGION_NAME = "chile" in s3_helpers but prompt says AWS_REGION)
    # CORS = ["*"] (current default in main.py)
    
    assert settings.S3_BUCKET_NAME == "pangu-mvp-data"
    # In s3_helpers.py, REGION_NAME was "chile". 
    # The prompt asks for AWS_REGION. 
    # NOTE: s3_helpers used "chile" for filename construction, NOT for boto3 region.
    # Boto3 region is usually implicit or "us-east-1". 
    # Let's verify what the prompt requested: "S3_BUCKET_NAME, AWS_REGION, CORS_ORIGINS".
    # We will use "us-east-1" as a safe AWS default, or maintain "chile" if context implies.
    # Looking at s3_helpers.py: REGION_NAME = "chile" # usado en el nombre del archivo
    # This suggests "chile" is part of the DATA SPEC, not necessarily the AWS Region.
    # HOWEVER, the prompt asks to extract `AWS_REGION`.
    # I will set a safe default like "us-east-1" for AWS_REGION, 
    # but I must check if `REGION_NAME` in `s3_helpers` is what the user meant.
    # The user said: "Extraé los siguientes valores... AWS_REGION". 
    # s3_helpers has `REGION_NAME = "chile"`.
    # It seems `REGION_NAME` is actually a data parameter. 
    # I will check if there is an actual AWS region usage. `s3_client = boto3.client("s3")` uses default.
    # I will assume the user wants to parameterize the AWS connection region OR the data region.
    # Given the name `AWS_REGION`, it implies the infra region. 
    
    assert isinstance(settings.CORS_ORIGINS, list)
    
    # We might expect ["*"] as default based on previous code which had allow_origins=["*"] as default?
    # Actually main.py has: `pydantic os.getenv("ALLOWED_ORIGINS", "*").split(",")`
    # So default should be ["*"]
    
    assert "*" in settings.CORS_ORIGINS or "http://localhost" in settings.CORS_ORIGINS
