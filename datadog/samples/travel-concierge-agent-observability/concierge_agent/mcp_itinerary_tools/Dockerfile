FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make entrypoint executable
RUN chmod +x entrypoint.sh

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create non-root user
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose port for MCP server
EXPOSE 8000

# Datadog LLM Observability via OTEL
# ddtrace-run auto-instruments botocore/MCP calls for Datadog
ENV DD_TRACE_ENABLED=true
ENV DD_LLMOBS_ENABLED=1
ENV DD_LLMOBS_AGENTLESS_ENABLED=1
ENV DD_LLMOBS_ML_APP=travel-concierge-agent
ENV DD_SERVICE=itinerary-mcp-server
ENV DD_ENV=demo
ENV DD_SITE=datadoghq.com

# Disable AgentCore's built-in ADOT — using Datadog instead
ENV DISABLE_ADOT_OBSERVABILITY=true

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run the MCP server — entrypoint resolves DD_API_KEY then runs ddtrace-run
CMD ["bash", "entrypoint.sh"]
