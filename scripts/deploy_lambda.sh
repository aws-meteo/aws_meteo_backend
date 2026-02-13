#!/usr/bin/env bash
set -euo pipefail

# Default values
AWS_REGION="${AWS_REGION:-us-east-1}"
ECR_REPO="${ECR_REPO:-aws-meteo-backend}"
FUNCTION_NAME="${FUNCTION_NAME:-aws-meteo-backend}"
IMAGE_TAG="${IMAGE_TAG:-latest}"
DRY_RUN="${DRY_RUN:-false}"

usage() {
    cat <<EOF
Usage: $0 [options]

Deploys the Docker image to AWS ECR and updates the Lambda function.
Assumes the Lambda function and ECR repository already exist.

Options:
  --dry-run          Print commands instead of executing them.
  -h, --help         Show this help message.

Environment Variables (with defaults):
  AWS_REGION        Default: $AWS_REGION
  ECR_REPO          Default: $ECR_REPO
  FUNCTION_NAME     Default: $FUNCTION_NAME
  IMAGE_TAG         Default: $IMAGE_TAG
  DRY_RUN           Default: $DRY_RUN

Example:
  AWS_REGION=eu-west-1 ./scripts/deploy_lambda.sh
EOF
}

# Parse arguments
while [[ $# -gt 0 ]]; do
    case "$1" in
        --dry-run)
            DRY_RUN=true
            ;;
        -h|--help)
            usage
            exit 0
            ;;
        *)
            echo "Error: Unknown argument $1"
            usage
            exit 1
            ;;
    esac
    shift
done

# Get AWS Account ID
if [[ "$DRY_RUN" == "true" ]]; then
    ACCOUNT_ID="123456789012"
else
    # Check if AWS CLI is installed and configured
    if ! command -v aws &> /dev/null; then
        echo "Error: aws cli is not installed." >&2
        exit 1
    fi
    ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
fi

ECR_URI="${ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${ECR_REPO}"

run_cmd() {
    if [[ "$DRY_RUN" == "true" ]]; then
        echo "[DRY-RUN] $*"
    else
        echo "[EXEC] $*"
        "$@"
    fi
}

echo "=== Deployment Configuration ==="
echo "AWS Region:    $AWS_REGION"
echo "ECR Repo:      $ECR_REPO"
echo "Function Name: $FUNCTION_NAME"
echo "Image Tag:     $IMAGE_TAG"
echo "ECR URI:       $ECR_URI"
echo "Dry Run:       $DRY_RUN"
echo "================================"

# 1. ECR Login
echo "Logging into Amazon ECR..."
if [[ "$DRY_RUN" == "true" ]]; then
    echo "[DRY-RUN] aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $ECR_URI"
else
    aws ecr get-login-password --region "$AWS_REGION" | docker login --username AWS --password-stdin "$ECR_URI"
fi

# 2. Tag local image
echo "Tagging local image..."
run_cmd docker tag "aws-meteo-backend:latest" "${ECR_URI}:${IMAGE_TAG}"

# 3. Push to ECR
echo "Pushing image to ECR..."
run_cmd docker push "${ECR_URI}:${IMAGE_TAG}"

# 4. Update Lambda Function
echo "Updating Lambda function code..."
run_cmd aws lambda update-function-code \
    --function-name "$FUNCTION_NAME" \
    --image-uri "${ECR_URI}:${IMAGE_TAG}" \
    --region "$AWS_REGION"

echo "Deployment finished successfully!"
