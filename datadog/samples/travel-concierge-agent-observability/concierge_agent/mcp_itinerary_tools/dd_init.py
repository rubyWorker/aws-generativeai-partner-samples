"""
Datadog LLM Observability initialization.

Resolves DD_API_KEY from Secrets Manager and enables LLM Observability.
Must be imported FIRST in every Python entry point (before any other imports).
"""
import os
import logging

logger = logging.getLogger(__name__)


def _resolve_dd_api_key():
    """Resolve DD_API_KEY from Secrets Manager if not already set."""
    secret_arn = os.environ.get("DD_API_KEY_SECRET_ARN")
    if not secret_arn or os.environ.get("DD_API_KEY"):
        return
    try:
        import boto3
        client = boto3.client("secretsmanager", region_name=os.environ.get("AWS_REGION", "us-east-1"))
        resp = client.get_secret_value(SecretId=secret_arn)
        os.environ["DD_API_KEY"] = resp["SecretString"]
        logger.info("DD_API_KEY resolved from Secrets Manager")
    except Exception as e:
        logger.error(f"Failed to resolve DD_API_KEY: {e}")


def _enable_llmobs():
    """Enable Datadog LLM Observability after API key is available."""
    try:
        from ddtrace.llmobs import LLMObs
        LLMObs.enable()
        logger.info("Datadog LLM Observability enabled")
    except Exception as e:
        logger.error(f"Failed to enable LLM Observability: {e}")


# Resolve API key first, then enable LLMObs
_resolve_dd_api_key()
_enable_llmobs()
