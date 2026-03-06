"""Resolve DD_API_KEY from Secrets Manager before ddtrace initializes."""
import os
import boto3
import logging

logger = logging.getLogger(__name__)

def _resolve_dd_api_key():
    secret_arn = os.environ.get("DD_API_KEY_SECRET_ARN")
    if not secret_arn or os.environ.get("DD_API_KEY"):
        return
    try:
        client = boto3.client("secretsmanager", region_name=os.environ.get("AWS_REGION", "us-east-1"))
        resp = client.get_secret_value(SecretId=secret_arn)
        os.environ["DD_API_KEY"] = resp["SecretString"]
        logger.info("DD_API_KEY resolved from Secrets Manager")
    except Exception as e:
        logger.error(f"Failed to resolve DD_API_KEY: {e}")

_resolve_dd_api_key()
