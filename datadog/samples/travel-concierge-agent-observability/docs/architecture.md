# Architecture — Datadog LLM Observability for AgentCore Travel Concierge Agent

## System Architecture

```mermaid
graph TB
    subgraph User Layer
        User([fa:fa-user User])
        WebUI[Web UI<br/>React + Amplify]
    end

    subgraph AgentCore Runtime
        Supervisor[Supervisor Agent<br/>Strands Agent + OTEL<br/><i>OTEL_SERVICE_NAME=supervisor-agent</i>]
        TravelSub[travel_assistant<br/>Strands Subagent]
    end

    subgraph AgentCore Gateway
        GW[Gateway<br/>IAM + MCP Routing]
    end

    subgraph MCP Servers — AgentCore Runtime
        TravelMCP[Travel MCP Server<br/>OTEL TracerProvider<br/><i>OTEL_SERVICE_NAME=travel-mcp-server</i>]
        ItineraryMCP[Itinerary MCP Server<br/>OTEL TracerProvider<br/><i>OTEL_SERVICE_NAME=itinerary-mcp-server</i>]
    end

    subgraph AWS Services
        Bedrock[Amazon Bedrock<br/>Claude Sonnet 4.5]
        DDB[(DynamoDB<br/>User Profiles · Itineraries)]
        Memory[AgentCore Memory<br/>Session History]
    end

    subgraph Datadog
        DDLLM[Datadog LLM Observability<br/>Prompts · Tokens · Latency · Tool Calls]
    end

    User -->|HTTPS| WebUI
    WebUI -->|SigV4 Auth| Supervisor
    Supervisor --> TravelSub
    Supervisor -->|Itinerary tools| GW
    TravelSub -->|travel tools| GW
    GW -->|MCP/HTTP| TravelMCP
    GW -->|MCP/HTTP| ItineraryMCP
    Supervisor -->|InvokeModel| Bedrock
    TravelSub -->|InvokeModel| Bedrock
    TravelMCP --> DDB
    ItineraryMCP --> DDB
    Supervisor --> Memory

    Supervisor -.->|OTLP over HTTPS| DDLLM
    TravelMCP -.->|OTLP over HTTPS| DDLLM
    ItineraryMCP -.->|OTLP over HTTPS| DDLLM

    classDef dd fill:#632CA6,stroke:#632CA6,color:#fff
    classDef aws fill:#FF9900,stroke:#FF9900,color:#fff
    classDef agent fill:#1A73E8,stroke:#1A73E8,color:#fff
    classDef mcp fill:#0D652D,stroke:#0D652D,color:#fff

    class DDLLM dd
    class Bedrock,DDB,Memory aws
    class Supervisor,TravelSub agent
    class TravelMCP,ItineraryMCP mcp
```

## Distributed Trace Flow

A single user request (e.g., *"Find flights from NYC to Tokyo"*) produces a distributed trace that spans every service in the system:

```mermaid
sequenceDiagram
    participant U as User / Web UI
    participant S as Supervisor Agent
    participant TS as travel_assistant (subagent)
    participant GW as AgentCore Gateway
    participant TMCP as Travel MCP Server
    participant B as Amazon Bedrock
    participant DD as Datadog LLM Obs

    U->>S: "Find flights from NYC to Tokyo"
    activate S
    Note over S: Root span: supervisor-agent

    S->>B: InvokeModel (routing decision)
    B-->>S: → delegate to travel_assistant

    S->>TS: travel_assistant(query)
    activate TS
    Note over TS: Child span: strands.agent.travel_assistant

    TS->>B: InvokeModel (plan tool calls)
    B-->>TS: → call travel_flight_search

    TS->>GW: MCP tool call: travel_flight_search
    GW->>TMCP: HTTP → travel-mcp-server
    activate TMCP
    Note over TMCP: Child span: travel-mcp-server

    TMCP->>TMCP: Execute flight search (SerpAPI)
    TMCP-->>GW: Flight results
    deactivate TMCP

    GW-->>TS: MCP response
    TS->>B: InvokeModel (format results)
    B-->>TS: Formatted flight options

    TS-->>S: Subagent response
    deactivate TS

    S-->>U: "Here are 5 flights from NYC to Tokyo..."
    deactivate S

    S-.>>DD: OTLP traces
    TMCP-.>>DD: OTLP traces
```

## Trace Hierarchy (Span Tree)

When viewed in Datadog LLM Observability, a typical request produces the following span hierarchy:

```
supervisor-agent                                    [root span — full request duration]
├── LLM: bedrock.converse (routing)                 [~1-3s — supervisor decides which subagent]
│   └── input_tokens: ~800, output_tokens: ~50
├── strands.tool: travel_assistant                  [subagent delegation span]
│   ├── LLM: bedrock.converse (plan)                [~1-2s — subagent plans tool calls]
│   │   └── input_tokens: ~1200, output_tokens: ~100
│   ├── MCP tool: travel_flight_search              [tool execution span]
│   │   └── travel-mcp-server                       [cross-service span]
│   │       └── HTTP: SerpAPI call                  [external API call]
│   ├── LLM: bedrock.converse (synthesize)          [~2-4s — format results]
│   │   └── input_tokens: ~3000, output_tokens: ~500
│   └── total_tokens: ~4800
└── total_tokens: ~5650
```

## OTEL Collection — Direct OTLP Export

All services use a custom OpenTelemetry `TracerProvider` with `OTLPSpanExporter` to send traces directly to Datadog's OTLP intake endpoint over HTTPS. No Datadog Agent sidecar is required.

```mermaid
graph LR
    subgraph AgentCore Runtime Containers
        SA[supervisor-agent<br/>python agent.py]
        T[travel-mcp-server<br/>python server.py]
        I[itinerary-mcp-server<br/>python server.py]
    end

    subgraph dd_init.py — OTEL Configuration
        TP[TracerProvider<br/>+ OTLPSpanExporter<br/>+ SimpleSpanProcessor]
    end

    subgraph Datadog OTLP Intake
        API["https://trace.agent.{DD_SITE}/v1/traces<br/>Headers: dd-api-key, dd-otlp-source=llmobs"]
    end

    SA --> TP
    T --> TP
    I --> TP
    TP -->|OTLP/HTTP| API
```

Each container's Dockerfile sets the required environment variables:

| Variable | Value | Purpose |
|----------|-------|---------|
| `DD_SITE` | `datadoghq.com` | Datadog site/region (determines OTLP endpoint) |
| `OTEL_SERVICE_NAME` | `supervisor-agent` / `travel-mcp-server` / etc. | Per-service name in LLM Observability |
| `OTEL_SEMCONV_STABILITY_OPT_IN` | `gen_ai_latest_experimental` | Enables GenAI semantic conventions (v1.37+) |
| `DISABLE_ADOT_OBSERVABILITY` | `true` | Disables AgentCore's built-in ADOT pipeline |
| `DD_API_KEY` | *(from Secrets Manager)* | Datadog API key for OTLP authentication |

The `DD_API_KEY` is retrieved at runtime from AWS Secrets Manager (`datadog/aig-agent/api-key`) by `entrypoint.sh` and used by `dd_init.py` to configure the `OTLPSpanExporter` headers.

### How dd_init.py Works

Each Python entry point imports `dd_init` as its first import. The module:

1. Sets `DISABLE_ADOT_OBSERVABILITY=true` and `OTEL_SEMCONV_STABILITY_OPT_IN=gen_ai_latest_experimental` via `os.environ.setdefault()`
2. Resolves `DD_API_KEY` from Secrets Manager (backup — `entrypoint.sh` does this first)
3. Creates an OpenTelemetry `Resource` with `service.name` from `OTEL_SERVICE_NAME`
4. Creates an `OTLPSpanExporter` targeting `https://trace.agent.{DD_SITE}/v1/traces` with headers `dd-api-key` and `dd-otlp-source=llmobs`
5. Creates a `TracerProvider` with a `SimpleSpanProcessor` and sets it as the global tracer provider

Once the `TracerProvider` is set, `strands-agents[otel]` automatically emits GenAI spans for every agent decision, planner step, tool call, and LLM invocation.

## Service Map

In Datadog LLM Observability, the deployed system renders as:

```
┌─────────────────────┐
│   supervisor-agent   │
│   (Strands Agent)    │
└──────┬──────────────┘
       │
       ├──────────────────────────┐
       │                          │
       ▼                          ▼
┌──────────────┐  ┌────────────────────┐
│ travel-mcp-  │  │  itinerary-mcp-    │
│   server     │  │     server         │
└──────┬───────┘  └────────┬───────────┘
       │                   │
       ▼                   ▼
┌──────────────────────────────────────────────────────────┐
│                    Amazon Bedrock                         │
│                  Claude Sonnet 4.5                        │
└──────────────────────────────────────────────────────────┘
```

All services share the same `DD_SITE` and `DD_API_KEY`, and their `OTEL_SERVICE_NAME` values distinguish them in the Datadog LLM Observability UI.
