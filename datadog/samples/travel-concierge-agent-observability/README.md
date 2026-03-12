# Datadog LLM Observability for Amazon Bedrock AgentCore Travel Concierge Agent

End-to-end observability for a multi-agent AI travel concierge, powered by [Datadog LLM Observability](https://docs.datadoghq.com/llm_observability/) and [Amazon Bedrock AgentCore](https://docs.aws.amazon.com/bedrock/latest/userguide/agentcore.html).

> **Note:** This sample is forked from the upstream [travel-concierge-agent](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/05-blueprints/travel-concierge-agent) blueprint and adds Datadog observability using the [AgentCore OTEL integration](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html) with `ddtrace`.

## What This Sample Demonstrates

- **OTEL-native LLM Observability** — Strands Agents emits [OpenTelemetry-compliant spans](https://www.datadoghq.com/blog/llm-aws-strands/) (GenAI semantic conventions) via `strands-agents[otel]`; Datadog's `ddtrace` auto-instruments and sends them to [Datadog LLM Observability](https://docs.datadoghq.com/llm_observability/setup/auto_instrumentation/)
- **AgentCore Integration** — Uses AgentCore's documented approach for [third-party observability platforms](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html): `DISABLE_ADOT_OBSERVABILITY=true` disables the built-in ADOT/CloudWatch pipeline so Datadog is the sole observability backend
- **APM Distributed Tracing** — A single user request produces a unified trace spanning `supervisor-agent` → `travel-mcp-server` / `itinerary-mcp-server` → Amazon Bedrock
- **Agentless Collection** — All traces are sent directly to Datadog's intake API over HTTPS — no Datadog Agent sidecar required
- **Troubleshooting Workflows** — Three documented scenarios showing how to debug slow tool calls, high token usage, and agent errors using Datadog's trace waterfall and LLM Observability views

## Architecture

The system uses a supervisor pattern: a Strands Agent (Claude Sonnet 4.5) delegates to `travel_assistant` subagent, which invokes MCP tools via AgentCore Gateway connecting to MCP servers.

![Architecture Diagram](docs/architecture.md)

For the full architecture diagram with Mermaid diagrams, trace flow, and span hierarchy, see **[docs/architecture.md](docs/architecture.md)**.

```
User → Web UI → (SigV4 via Cognito guest creds) → AgentCore Runtime (Supervisor + ddtrace + OTEL spans)
                                                          │
                                                          ├── travel_assistant → AgentCore Gateway → Travel MCP Server (ddtrace)
                                                          └── itinerary tools  → AgentCore Gateway → Itinerary MCP Server (ddtrace)
                                                                                                           │
                                                                                                     Amazon Bedrock
                                                                                                    (Claude Sonnet 4.5)

        DISABLE_ADOT_OBSERVABILITY=true  (AgentCore's built-in CloudWatch pipeline is off)
        All services ──(agentless HTTPS)──→ Datadog LLM Observability
```

### How the OTEL Integration Works

1. **`strands-agents[otel]`** — Installed in the supervisor agent, this makes Strands emit OTEL-compliant spans following [GenAI semantic conventions](https://opentelemetry.io/docs/specs/semconv/gen-ai/) for every agent decision, planner step, tool call, and LLM invocation
2. **`ddtrace`** — Datadog's tracer [auto-instruments Strands Agents](https://docs.datadoghq.com/llm_observability/setup/auto_instrumentation/) (>= 1.11.0), capturing those OTEL spans and forwarding them to Datadog LLM Observability
3. **`DISABLE_ADOT_OBSERVABILITY=true`** — Per [AgentCore docs](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html), this disables the default ADOT/CloudWatch pipeline so `ddtrace` is the sole instrumentation layer
4. **Agentless mode** — `DD_LLMOBS_AGENTLESS_ENABLED=1` sends traces directly to Datadog's intake API over HTTPS, no Datadog Agent sidecar needed

## Prerequisites

| Requirement | Details |
|-------------|---------|
| **AWS Account** | With permissions for Bedrock AgentCore, Amplify, CDK, DynamoDB, ECR, Secrets Manager |
| **Datadog Account** | With [LLM Observability](https://docs.datadoghq.com/llm_observability/) enabled |
| **Secrets Manager Secrets** | `datadog/aig-agent/api-key` and `datadog/aig-agent/app-key` must exist in your AWS account |
| **Node.js** | v18+ (v20 recommended) |
| **Docker / Finch** | For building agent container images. If using Finch, set `export CDK_DOCKER=finch` before deploying |
| **AWS CLI** | v2+ configured with credentials |
| **jq** | `brew install jq` (macOS) or `apt-get install jq` (Linux) |

### Datadog Secrets Setup

The Datadog API key must be stored in AWS Secrets Manager before deployment. The CDK stacks reference this secret to inject `DD_API_KEY` into the container environment at runtime via `entrypoint.sh`.

```bash
# Verify the secret exists
aws secretsmanager describe-secret --secret-id datadog/aig-agent/api-key
```

## Quick Start

```bash
# 1. Install dependencies
npm install
cd amplify && npm install && cd ..

# 2. Deploy Amplify backend (DynamoDB, AppSync, Cognito Identity Pool)
npm run deploy:amplify

# 3. Deploy MCP servers (Travel, Itinerary — each with ddtrace)
# If using Finch instead of Docker:
export CDK_DOCKER=finch
npm run deploy:mcp

# 4. Deploy supervisor agent (with strands-agents[otel] + ddtrace)
npm run deploy:agent

# 5. Configure web UI environment (auto-populates from CloudFormation outputs)
./scripts/setup-web-ui-env.sh --force

# 6. Start local dev server
npm run dev
```

Access the application at `https://localhost:9000/`

### Cognito Guest Access (AgentCore Auth)

The web UI calls AgentCore Runtime directly from the browser using SigV4-signed requests. Temporary AWS credentials are obtained via a Cognito Identity Pool configured for unauthenticated (guest) access.

The Amplify backend (`amplify/backend.ts`) creates:
- A **Cognito Identity Pool** with `allowUnauthenticatedIdentities: true`
- An **IAM role** for guest users with `bedrock-agentcore:InvokeAgentRuntime` and `bedrock-agentcore:InvokeAgentRuntimeWithResponseStream` permissions
- A **role attachment** mapping the unauthenticated role to the identity pool
- **Classic auth flow** enabled (`allowClassicFlow: true`) to avoid session policy restrictions

After deploying the Amplify backend, the Identity Pool ID and Guest Role ARN must be set in `web-ui/.env.local`:

```bash
VITE_IDENTITY_POOL_ID=us-east-1:xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
VITE_GUEST_ROLE_ARN=arn:aws:iam::123456789012:role/amplify-...-GuestUnauthRole-...
```

Running `./scripts/setup-web-ui-env.sh --force` will auto-populate this from CloudFormation outputs.

### Datadog Environment Variables

Each container's Dockerfile includes the Datadog instrumentation configuration. These are baked into the image and do not need to be set manually:

```dockerfile
# Datadog LLM Observability via OTEL
ENV DD_TRACE_ENABLED=true
ENV DD_LLMOBS_ENABLED=1
ENV DD_LLMOBS_AGENTLESS_ENABLED=1
ENV DD_LLMOBS_ML_APP=travel-concierge-agent
ENV DD_SERVICE=supervisor-agent          # varies per container
ENV DD_ENV=demo
ENV DD_SITE=datadoghq.com

# Disable AgentCore's built-in ADOT — using Datadog instead
ENV DISABLE_ADOT_OBSERVABILITY=true
```

Per the [AgentCore docs on using other observability platforms](https://docs.aws.amazon.com/bedrock-agentcore/latest/devguide/observability-configure.html), `DISABLE_ADOT_OBSERVABILITY=true` unsets AgentCore's default ADOT environment variables so `ddtrace` is the sole instrumentation layer.

The `DD_API_KEY` is resolved at runtime from Secrets Manager. Each container uses an `entrypoint.sh` that fetches the key before launching `ddtrace-run`:

```bash
# entrypoint.sh resolves DD_API_KEY, then:
exec ddtrace-run python agent.py   # supervisor
exec ddtrace-run python server.py  # MCP servers
```

The `dd_init.py` module (imported first in each Python entry point) provides a backup resolution of `DD_API_KEY` and calls `LLMObs.enable()` to activate Datadog LLM Observability.

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
│   ├── supervisor_agent/          # Supervisor agent (Strands + strands-agents[otel] + ddtrace)
│   │   ├── Dockerfile             # ddtrace-run entrypoint, DISABLE_ADOT_OBSERVABILITY=true
│   │   ├── dd_init.py             # Resolves DD_API_KEY + enables LLMObs
│   │   ├── entrypoint.sh          # Resolves DD_API_KEY from Secrets Manager, runs ddtrace-run
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
├── amplify/                       # Amplify backend (DynamoDB, GraphQL, Cognito Identity Pool)
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
| Supervisor Agent | `concierge_agent/supervisor_agent` | `supervisor-agent` | `strands-agents[otel]` emits OTEL spans; `ddtrace-run` auto-instruments Strands (>= 1.11.0), `botocore` (Bedrock calls) |
| Travel MCP Server | `concierge_agent/mcp_travel_tools` | `travel-mcp-server` | `ddtrace-run` auto-instruments `botocore` + `requests` (SerpAPI, Google Maps) + `mcp` |
| Itinerary MCP Server | `concierge_agent/mcp_itinerary_tools` | `itinerary-mcp-server` | `ddtrace-run` auto-instruments `botocore` (DynamoDB) + `mcp` |

## Cleanup

```bash
# Remove all deployed AWS resources
npm run clean
```

See the [Deployment Guide — Clean Up](DEPLOYMENT.md#clean-up) for partial cleanup options.

---

> **Disclaimer:** This project is provided as a sample implementation for educational and demonstration purposes. It is NOT production ready. Please ensure compliance with your organization's policies and AWS service terms.
