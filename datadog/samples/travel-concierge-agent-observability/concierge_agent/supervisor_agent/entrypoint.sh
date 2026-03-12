#!/bin/bash
# Resolve DD_API_KEY from Secrets Manager before starting ddtrace-run
# This ensures the API key is available as an env var when ddtrace initializes

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

exec ddtrace-run python agent.py
