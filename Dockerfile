FROM public.ecr.aws/lambda/python:3.12

# AWS Lambda Web Adapter for HTTP event translation
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.9.1 /lambda-adapter /opt/extensions/lambda-adapter
ENV PORT=8000

# Install dependencies using binary wheels to avoid source compilation
WORKDIR ${LAMBDA_TASK_ROOT}
COPY api_requirements.txt .
RUN pip install --no-cache-dir -r api_requirements.txt

# Copy application code to the Lambda task root
COPY app/ ${LAMBDA_TASK_ROOT}/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
