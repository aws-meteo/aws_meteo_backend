#!/usr/bin/env bash
set -euo pipefail

# Default values
AWS_PROFILE=${AWS_PROFILE:-default}
AWS_REGION=${AWS_REGION:-us-east-1}
S3_BUCKET_NAME=${S3_BUCKET_NAME:-pangu-mvp-data}
IMAGE_NAME="aws-meteo-backend"

# Support passing a profile name as an argument
if [[ $# -ge 1 ]]; then
    if [[ "$1" == "-h" || "$1" == "--help" ]]; then
        cat <<EOF
Usage: $0 [profile_name]

Runs the docker container with local AWS credentials and environment variables.
Default AWS_PROFILE: $AWS_PROFILE
Default AWS_REGION: $AWS_REGION
Default S3_BUCKET_NAME: $S3_BUCKET_NAME
EOF
        exit 0
    fi
    AWS_PROFILE="$1"
fi

# Handle the case where \$HOME/.aws doesn't exist (warning)
if [[ ! -d "$HOME/.aws" ]]; then
    echo "Warning: \$HOME/.aws directory not found. Local AWS credentials will not be mounted correctly if missing." >&2
fi

# Print the command it's about to run
echo "Running command:"
echo "docker run --rm -p 8000:8000 \\"
echo "  -e AWS_PROFILE=$AWS_PROFILE \\"
echo "  -e AWS_REGION=$AWS_REGION \\"
echo "  -e S3_BUCKET_NAME=$S3_BUCKET_NAME \\"
echo "  -v \"\$HOME/.aws:/root/.aws:ro\" \\"
echo "  $IMAGE_NAME"

# Run docker
docker run --rm -p 8000:8000 \
    -e AWS_PROFILE="$AWS_PROFILE" \
    -e AWS_REGION="$AWS_REGION" \
    -e S3_BUCKET_NAME="$S3_BUCKET_NAME" \
    -v "$HOME/.aws:/root/.aws:ro" \
    "$IMAGE_NAME"
