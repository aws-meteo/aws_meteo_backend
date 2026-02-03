from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from typing import List, Union

class Settings(BaseSettings):
    S3_BUCKET_NAME: str = "pangu-mvp-data"
    AWS_REGION: str = "us-east-1"
    # Use Union to allow pydantic-settings to read it as a string from env, 
    # then validator converts to list.
    CORS_ORIGINS: Union[List[str], str] = ["*"]
    
    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        if isinstance(v, str):
            # If it looks like a list repr, ignore (pydantic might handle), 
            # but we assume CSV for standard Env vars
            if not v.strip().startswith("["):
                 return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8"
    )

settings = Settings()
