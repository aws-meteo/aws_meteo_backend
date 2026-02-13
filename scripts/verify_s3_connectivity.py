import sys
import os
import boto3
import argparse
from botocore.exceptions import NoCredentialsError, PartialCredentialsError, EndpointConnectionError, ClientError

# Add the current directory to sys.path to import app.config
sys.path.append(os.getcwd())

try:
    from app.config import settings
except ImportError:
    print("ERROR: Could not import app.config. Ensure you are running this script from the project root.")
    sys.exit(1)

def verify_s3():
    bucket = settings.S3_BUCKET_NAME
    region = settings.AWS_REGION
    prefix = "indices/sti/"
    
    print(f"--- AWS S3 Connectivity Verification ---")
    print(f"Configured Bucket: {bucket}")
    print(f"Configured Region: {region}")
    print(f"Target Prefix: {prefix}")
    print("-" * 40)

    try:
        # Check STS Identity
        sts = boto3.client('sts', region_name=region)
        identity = sts.get_caller_identity()
        print(f"SUCCESS: AWS Identity found.")
        print(f"Account: {identity.get('Account')}")
        print(f"UserId: {identity.get('UserId')}")
        print(f"Arn: {identity.get('Arn')}")
        print("-" * 40)

        # List objects
        s3 = boto3.client('s3', region_name=region)
        print(f"Attempting to list objects in '{bucket}' under '{prefix}'...")
        
        response = s3.list_objects_v2(
            Bucket=bucket,
            Prefix=prefix,
            Delimiter='/',
            MaxKeys=10
        )

        if 'CommonPrefixes' in response:
            print(f"SUCCESS: Found {len(response['CommonPrefixes'])} top-level folders:")
            for cp in response['CommonPrefixes']:
                print(f" - {cp['Prefix']}")
        elif 'Contents' in response:
            print(f"SUCCESS: Found {len(response['Contents'])} objects.")
        else:
            print("WARNING: Connected successfully, but no objects found with the given prefix.")

    except NoCredentialsError:
        print("ERROR: No AWS credentials found. Please configure your environment (e.g., via AWS_ACCESS_KEY_ID/AWS_SECRET_ACCESS_KEY or ~/.aws/credentials).")
    except PartialCredentialsError:
        print("ERROR: Incomplete AWS credentials found. Please check your configuration.")
    except EndpointConnectionError:
        print(f"ERROR: Could not connect to the AWS endpoint. Check your internet connection and region ('{region}').")
    except ClientError as e:
        error_code = e.response.get('Error', {}).get('Code')
        if error_code == 'AccessDenied':
            print(f"ERROR: Access Denied to bucket '{bucket}'. Ensure your IAM policy allows 's3:ListBucket' on 'arn:aws:s3:::{bucket}'.")
        elif error_code == 'NoSuchBucket':
            print(f"ERROR: The bucket '{bucket}' does not exist.")
        else:
            print(f"ERROR: AWS ClientError: {e}")
    except Exception as e:
        print(f"ERROR: An unexpected error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify connectivity to AWS S3 and check access to the configured bucket and prefix.")
    args = parser.parse_args()
    
    verify_s3()
