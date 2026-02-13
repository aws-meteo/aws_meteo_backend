import boto3
import fsspec
from ..config import settings

def get_s3_client():
    """
    Returns a boto3 S3 client using the configured AWS region.
    """
    return boto3.client("s3", region_name=settings.AWS_REGION)

def get_s3_fs():
    """
    Returns an fsspec S3 filesystem instance.
    """
    return fsspec.filesystem("s3")
