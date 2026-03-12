FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim
WORKDIR /app

# Configure UV for container environment
ENV UV_SYSTEM_PYTHON=1 UV_COMPILE_BYTECODE=1

# Copy requirements and install dependencies
COPY requirements.txt .
RUN uv pip install -r requirements.txt

# Set environment variables
ENV AWS_REGION=us-east-1
ENV AWS_DEFAULT_REGION=us-east-1
ENV DOCKER_CONTAINER=1
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Datadog LLM Observability via OTEL
# strands-agents[otel] emits OTEL spans; ddtrace-run captures them for Datadog
ENV DD_TRACE_ENABLED=true
ENV DD_LLMOBS_ENABLED=1
ENV DD_LLMOBS_AGENTLESS_ENABLED=1
ENV DD_LLMOBS_ML_APP=travel-concierge-agent
ENV DD_SERVICE=supervisor-agent
ENV DD_ENV=demo
ENV DD_SITE=datadoghq.com

# Disable AgentCore's built-in ADOT — using Datadog instead
ENV DISABLE_ADOT_OBSERVABILITY=true

# Copy application code
COPY . .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Create non-root user
RUN useradd -m -u 1000 bedrock_agentcore && \
    chown -R bedrock_agentcore:bedrock_agentcore /app
USER bedrock_agentcore

# Expose ports
EXPOSE 8080
EXPOSE 8000

# Add HEALTHCHECK 
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
  CMD pgrep -f "python agent.py" || exit 1

# Run the agent — entrypoint resolves DD_API_KEY then runs ddtrace-run
CMD ["bash", "entrypoint.sh"]