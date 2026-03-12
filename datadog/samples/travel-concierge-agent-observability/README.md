# Datadog LLM Observability for Amazon Bedrock AgentCore Travel Concierge Agent

End-to-end observability for a multi-agent AI travel concierge, powered by [Datadog LLM Observability](https://docs.datadoghq.com/llm_observability/) and [Amazon Bedrock AgentCore](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore.html).

> **Note:** This sample is forked from the upstream [travel-concierge-agent](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/05-blueprints/travel-concierge-agent) blueprint and adds Datadog `ddtrace` instrumentation across all agent and MCP server containers.

## What This Sample Demonstrates

- **LLM Observability** — Every Bedrock LLM call (supervisor + subagents) is traced with prompts, completions, token usage, and latency via `ddtrace` auto-instrumentation of `botocore` and `strands-agents`
- **APM Distributed Tracing** — A single user request produces a unified trace spanning `supervisor-agent` → `travel-mcp-server` / `itinerary-mcp-server` → Amazon Bedrock
- **Agentless Collection** — All traces are sent directly to Datadog's intake API over HTTPS — no Datadog Agent sidecar required
- **Troubleshooting Workflows** — Three documented scenarios showing how to debug slow tool calls, high token usage, and agent errors using Datadog's trace waterfall and LLM Observability views

## Architecture

The system uses a supervisor pattern: a Strands Agent (Claude Sonnet 4.5) delegates to `travel_assistant` subagent, which invokes MCP tools via AgentCore Gateway connecting to MCP servers.

![Architecture Diagram](docs/architecture.md)

For the full architecture diagram with Mermaid diagrams, trace flow, and span hierarchy, see **[docs/architecture.md](docs/architecture.md)**.

```
User → Web UI → AgentCore Runtime (Supervisor + ddtrace)
                        │
                        ├── travel_assistant → AgentCore Gateway → Travel MCP Server (ddtrace)
                        └── itinerary tools  → AgentCore Gateway → Itinerary MCP Server (ddtrace)
                                                                          │
                                                                    Amazon Bedrock
                                                                   (Claude Sonnet 4.5)

        All services ──(agentless)──→ Datadog APM + LLM Observability
```

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **AWS Account** | With permissions for Bedrock AgentCore, Amplify, CDK, DynamoDB, ECR, Secrets Manager |
| **Datadog Account** | With [LLM Observability](https://docs.datadoghq.com/llm_observability/) enabled |
| **Secrets Manager Secrets** | `datadog/aig-agent/api-key` and `datadog/aig-agent/app-key` must exist in your AWS account |
| **Node.js** | v18+ (v20 recommended) |
| **Docker** | For building agent container images |
| **AWS CLI** | v2+ configured with credentials |
| **jq** | `brew install jq` (macOS) or `apt-get install jq` (Linux) |

### Datadog Secrets Setup

The Datadog API key and App key must be stored in AWS Secrets Manager before deployment. The CDK stacks and Dockerfiles reference these secrets to inject `DD_API_KEY` into the container environment at runtime.

```bash
# Verify the secrets exist
aws secretsmanager describe-secret --secret-id datadog/aig-agent/api-key
aws secretsmanager describe-secret --secret-id datadog/aig-agent/app-key
```

## Quick Start

```bash
# 1. Install dependencies
npm install
cd amplify && npm install && cd ..

# 2. Deploy Amplify backend (DynamoDB, AppSync)
npm run deploy:amplify

# 3. Deploy MCP servers (Travel, Itinerary — each with ddtrace)
npm run deploy:mcp

# 4. Deploy supervisor agent (with ddtrace + Datadog env vars)
npm run deploy:agent

# 5. Start local dev server
npm run dev
```

Access the application at `https://localhost:9000/`

### Datadog Environment Variables

Each container's Dockerfile includes the Datadog instrumentation configuration. These are baked into the image and do not need to be set manually:

```dockerfile
ENV DD_TRACE_ENABLED=true
ENV DD_LLMOBS_ENABLED=1
ENV DD_LLMOBS_AGENTLESS_ENABLED=1
ENV DD_LLMOBS_ML_APP=travel-concierge-agent
ENV DD_SERVICE=supervisor-agent          # varies per container
ENV DD_ENV=demo
ENV DD_SITE=datadoghq.com
```

AgentCore Runtime includes built-in ADOT (AWS Distro for OpenTelemetry) instrumentation. Since this sample uses Datadog's `ddtrace` instead, we disable ADOT to prevent conflicts:

```dockerfile
ENV DISABLE_ADOT_OBSERVABILITY=true
```

This is set in all Dockerfiles and CDK environment variables. See [AWS docs on using other observability platforms](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html) for details.

The `DD_API_KEY` is injected at runtime from Secrets Manager via `dd_init.py` (imported first in each Python entry point). Each container's entrypoint is wrapped with `ddtrace-run`:

```dockerfile
CMD ["ddtrace-run", "python", "agent.py"]   # supervisor
CMD ["ddtrace-run", "python", "server.py"]  # MCP servers
```

### Verifying Traces

After deploying and sending a test message through the Web UI:

1. Open **Datadog → APM → Traces**
2. Filter by `service:supervisor-agent`
3. You should see traces with child spans for subagent delegations, MCP tool calls, and Bedrock LLM invocations
4. Open **Datadog → LLM Observability** and filter by `ml_app:travel-concierge-agent` to see prompts, completions, and token usage

## Project Structure

```
travel-concierge-agent-observability/
├── concierge_agent/
│   ├── supervisor_agent/          # Supervisor agent (Strands + ddtrace)
│   │   ├── Dockerfile             # ddtrace-run entrypoint + DD_* env vars
│   │   ├── agent.py               # Main agent with BedrockModel (Claude 4.5)
│   │   ├── travel_subagent.py     # Travel planning subagent
│   │   └── gateway_client.py      # MCP Gateway client (OAuth2)
│   ├── mcp_travel_tools/          # Travel MCP server (ddtrace)
│   └── mcp_itinerary_tools/       # Itinerary MCP server (ddtrace)
├── infrastructure/
│   ├── agent-stack/               # CDK for supervisor agent + gateway
│   ├── mcp-servers/               # CDK for MCP server runtimes
│   └── frontend-stack/            # CDK for web UI hosting
├── web-ui/                        # React frontend (Amplify)
├── amplify/                       # Amplify backend (DynamoDB, GraphQL)
├── docs/
│   ├── architecture.md            # Mermaid architecture diagrams
│   └── troubleshooting-guide.md   # 3 debugging scenarios with Datadog
├── PRD.md                         # Product requirements document
├── DEPLOYMENT.md                  # Detailed deployment guide
└── README.md                      # ← You are here
```

## Documentation

| Document | Description |
|----------|-------------|
| **[Architecture](docs/architecture.md)** | Mermaid diagrams: system architecture, distributed trace flow, span hierarchy, agentless collection |
| **[Troubleshooting Guide](docs/troubleshooting-guide.md)** | Three scenarios: slow flight search, high token usage, agent error debugging |
| **[Deployment Guide](DEPLOYMENT.md)** | Step-by-step deployment instructions, configuration, and cleanup |
| **[PRD](PRD.md)** | Product requirements document for this observability sample |
| **[Infrastructure](infrastructure/README.md)** | CDK stack details and configuration |

## Instrumented Services

| Service | Container | DD_SERVICE | Instrumentation |
|---------|-----------|------------|-----------------|
| Supervisor Agent | `concierge_agent/supervisor_agent` | `supervisor-agent` | `ddtrace-run` auto-patches `botocore` (Bedrock calls) + `strands-agents` (workflow spans) |
| Travel MCP Server | `concierge_agent/mcp_travel_tools` | `travel-mcp-server` | `ddtrace-run` auto-patches `botocore` + `requests` (SerpAPI, Google Maps) |
| Itinerary MCP Server | `concierge_agent/mcp_itinerary_tools` | `itinerary-mcp-server` | `ddtrace-run` auto-patches `botocore` (DynamoDB) |

## Cleanup

```bash
# Remove all deployed AWS resources
npm run clean
```

See the [Deployment Guide — Clean Up](DEPLOYMENT.md#clean-up) for partial cleanup options.

---

> **Disclaimer:** This project is provided as a sample implementation for educational and demonstration purposes. It is NOT production ready. Please ensure compliance with your organization's policies and AWS service terms.
