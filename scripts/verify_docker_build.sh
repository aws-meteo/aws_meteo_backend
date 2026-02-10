#!/usr/bin/env bash
set -euo pipefail

IMAGE_NAME="aws-meteo-backend"
MODE="build-and-test"

usage() {
  cat <<'EOF'
Usage: ./scripts/verify_docker_build.sh [--build-only|--test-only] [image-name]

Default behavior (no flags): build image and run tests in container.

Test command:
  docker run --rm -e PYTHONPATH=/var/task/app -w /var/task --entrypoint python aws-meteo-backend \
    -m pytest -k "not pangu" \
    --ignore=app/lib/tests/test_xarray_utils.py \
    --ignore=app/lib/tests/test_pangu_pipeline.py

Notes:
  --build-only  Build image only.
  --test-only   Run tests only (requires an existing image).
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --build-only)
      if [[ "$MODE" != "build-and-test" ]]; then
        echo "[verify] error: --build-only and --test-only are mutually exclusive" >&2
        exit 1
      fi
      MODE="build-only"
      ;;
    --test-only)
      if [[ "$MODE" != "build-and-test" ]]; then
        echo "[verify] error: --build-only and --test-only are mutually exclusive" >&2
        exit 1
      fi
      MODE="test-only"
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --*)
      echo "[verify] error: unknown flag '$1'" >&2
      usage >&2
      exit 1
      ;;
    *)
      if [[ "$IMAGE_NAME" != "aws-meteo-backend" ]]; then
        echo "[verify] error: image name provided more than once" >&2
        usage >&2
        exit 1
      fi
      IMAGE_NAME="$1"
      ;;
  esac
  shift
done

build_image() {
  echo "[verify] docker build -t ${IMAGE_NAME} ."
  docker build -t "${IMAGE_NAME}" .
}

run_tests() {
  echo "[verify] docker run --rm -e PYTHONPATH=/var/task/app -w /var/task --entrypoint python ${IMAGE_NAME} -m pytest -k \"not pangu\" --ignore=app/lib/tests/test_xarray_utils.py --ignore=app/lib/tests/test_pangu_pipeline.py"
  docker run --rm -e PYTHONPATH=/var/task/app -w /var/task --entrypoint python "${IMAGE_NAME}" \
    -m pytest -k "not pangu" \
    --ignore=app/lib/tests/test_xarray_utils.py \
    --ignore=app/lib/tests/test_pangu_pipeline.py
}

case "$MODE" in
  build-only)
    build_image
    ;;
  test-only)
    run_tests
    ;;
  build-and-test)
    build_image
    run_tests
    ;;
esac

echo "[verify] OK"
