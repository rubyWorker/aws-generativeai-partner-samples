#!/bin/bash
# Entrypoint for MCP itinerary tools — Datadog-only observability via OTEL.
#
# How it works:
# 1. ddtrace-run auto-instruments botocore/MCP calls and sends to Datadog LLM Observability
# 2. DISABLE_ADOT_OBSERVABILITY=true prevents AgentCore's ADOT from conflicting
#
# Resolves DD_API_KEY from Secrets Manager before starting.

if [ -n "$DD_API_KEY_SECRET_ARN" ] && [ -z "$DD_API_KEY" ]; then
    echo "Resolving DD_API_KEY from Secrets Manager..."
    export DD_API_KEY=$(python -c "
import boto3, os
client = boto3.client('secretsmanager', region_name=os.environ.get('AWS_REGION', 'us-east-1'))
print(client.get_secret_value(SecretId=os.environ['DD_API_KEY_SECRET_ARN'])['SecretString'])
" 2>/dev/null)
    if [ -n "$DD_API_KEY" ]; then
        echo "DD_API_KEY resolved successfully"
    else
        echo "WARNING: Failed to resolve DD_API_KEY from Secrets Manager"
    fi
fi

exec ddtrace-run python server.py
