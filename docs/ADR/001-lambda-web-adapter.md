# ADR 001: AWS Lambda Web Adapter for FastAPI

## Status
Accepted

## Context
We are migrating a FastAPI application to AWS Lambda. The previous implementation used Mangum as a wrapper to translate Lambda events to ASGI. This approach added overhead and made local development different from the production environment.

## Decision
We have decided to use the AWS Lambda Web Adapter (ALWA). This allows us to run the FastAPI application using standard tools like Uvicorn inside the container. ALWA runs as a Lambda Extension and provides a transparent HTTP proxy.

## Consequences
- **Portability**: The same container image can run on Lambda, EC2, or locally without code changes.
- **Simplicity**: No need for Mangum or custom Lambda handlers.
- **Performance**: ALWA is highly optimized and written in Rust.
- **Standardization**: Uses standard HTTP/ASGI patterns throughout the stack.
