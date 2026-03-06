# PRD: Datadog Observability for Amazon Bedrock AgentCore Travel Concierge Agent

**Status:** APPROVED  
**Author:** AI Research Subagent  
**Date:** 2025-07-15  
**Location:** `datadog/travel-concierge-agent-observability/`

---

## 1. Overview

### Problem Statement

Developers building agentic AI applications on Amazon Bedrock AgentCore lack practical guidance on how to instrument, monitor, and troubleshoot multi-agent workflows using third-party observability tools. When an agent chain fails — a flight search times out, a subagent hallucinates, or token costs spike — operators have no unified view to diagnose root causes across the supervisor → subagent → MCP tool call chain.

### Solution Summary

Create a polished partner sample that forks the [AWS Bedrock AgentCore travel-concierge-agent](https://github.com/awslabs/amazon-bedrock-agentcore-samples/tree/main/05-blueprints/travel-concierge-agent) and instruments it with Datadog's `ddtrace` library to enable:

1. **LLM Observability** — End-to-end tracing of every LLM call (supervisor + subagents), capturing prompts, completions, token usage, latency, and errors
2. **APM Distributed Tracing** — Service map showing supervisor_agent → travel_subagent → MCP gateway → Bedrock, with latency breakdown per span
3. **Troubleshooting Workflows** — Documented scenarios showing how to use Datadog dashboards and trace views to debug real-world agentic AI issues

### Source Application Architecture

The travel-concierge-agent is a multi-agent system built with:
- **Strands Agents SDK** (`strands-agents`) for agent orchestration
- **Bedrock AgentCore Runtime** for containerized deployment
- **MCP (Model Context Protocol)** tools via AgentCore Gateway
- **Claude Sonnet 4.5** as the LLM backbone
- **Supervisor pattern**: `agent.py` (supervisor) → `travel_subagent.py` + `cart_subagent.py` (subagents) → MCP tool servers (travel, cart, itinerary)

Key Python files:
- `concierge_agent/supervisor_agent/agent.py` — Main supervisor agent entry point
- `concierge_agent/supervisor_agent/travel_subagent.py` — Travel planning subagent
- `concierge_agent/supervisor_agent/cart_subagent.py` — Cart/payment subagent
- `concierge_agent/supervisor_agent/gateway_client.py` — MCP Gateway client
- `concierge_agent/mcp_travel_tools/server.py` — MCP travel tools server
- `concierge_agent/mcp_cart_tools/` — MCP cart tools server
- `concierge_agent/mcp_itinerary_tools/` — MCP itinerary tools server
- `infrastructure/agent-stack/` — CDK for supervisor agent deployment
- `infrastructure/mcp-servers/` — CDK for MCP server deployment

---

## 2. Goals

| # | Goal | Metric |
|---|------|--------|
| G1 | Demonstrate Datadog LLM Observability capturing every Bedrock LLM call with input/output, tokens, latency | Traces visible in Datadog LLM Observability UI with all span types |
| G2 | Show distributed tracing across supervisor → subagent → MCP tool → Bedrock | Service map renders all 4+ services with connected spans |
| G3 | Provide 3+ documented troubleshooting scenarios with Datadog screenshots/guidance | README includes step-by-step debugging walkthroughs |
| G4 | Zero-friction setup: `DD_API_KEY` + `DD_SITE` are the only required Datadog config | Deploy instructions work with just env vars |
| G5 | Sample is demo-quality: polished README, architecture diagram, clean code | Passes partner sample review bar |

---

## 3. Non-Goals

- **NG1:** Building a new agent from scratch — we fork/adapt the existing travel-concierge-agent
- **NG2:** Modifying the React web-ui frontend — instrumentation is backend-only (Python agent code)
- **NG3:** Implementing Datadog RUM for the frontend
- **NG4:** Creating custom Datadog dashboards via API/Terraform — we rely on OOTB LLM Observability dashboards
- **NG5:** Modifying the CDK infrastructure stacks — we only add Datadog env vars to existing constructs
- **NG6:** Supporting non-Datadog observability backends

---

## 4. Background & Research

### 4.1 Datadog LLM Observability for Bedrock

From [Datadog docs](https://docs.datadoghq.com/llm_observability/):
- **Auto-instrumentation**: `ddtrace` automatically patches `botocore` (the AWS SDK used by `strands-agents` via `BedrockModel`) to capture Bedrock `InvokeModel`/`Converse` calls
- **Span types**: LLM spans capture `input`, `output`, `token_usage` (input/output/total), `model_id`, `model_provider`, latency, and errors
- **Agent Monitoring**: Datadog's Agent Monitoring view shows agentic workflows as hierarchical traces with workflow → agent → tool → LLM spans
- **Strands integration**: Datadog blog confirms native support for Strands Agents workflows ([blog post](https://www.datadoghq.com/blog/llm-aws-strands))
- **Bedrock Agents blog**: Datadog has a dedicated blog on monitoring Bedrock agents ([blog post](https://www.datadoghq.com/blog/llm-observability-bedrock-agents/))

### 4.2 ddtrace Python Integration

Key configuration via environment variables:
```
DD_TRACE_ENABLED=true
DD_SERVICE=travel-concierge-agent
DD_ENV=demo
DD_VERSION=1.0.0
DD_LLMOBS_ENABLED=1
DD_LLMOBS_ML_APP=travel-concierge-agent
DD_LLMOBS_AGENTLESS_ENABLED=1   # For containerized deployments without DD Agent sidecar
DD_API_KEY=<your-key>
DD_SITE=datadoghq.com
```

The `ddtrace-run` command or `ddtrace.patch_all()` auto-patches:
- `botocore` — captures Bedrock API calls (InvokeModel, Converse, ConverseStream)
- `strands-agents` — captures agent workflow spans (if supported, else manual annotation)

### 4.3 Instrumentation Strategy

**Primary approach: `ddtrace` auto-instrumentation + minimal manual annotation**

1. Add `ddtrace` to `requirements.txt` for supervisor_agent and each MCP server
2. Wrap the container entrypoint with `ddtrace-run` in each Dockerfile
3. Set DD env vars in CDK agent-stack and mcp-servers stack
4. Add manual `LLMObs` annotations only where auto-instrumentation gaps exist (e.g., custom tool spans, subagent delegation boundaries)

This approach is minimally invasive — the core agent logic remains unchanged.

---

## 5. Requirements

### R1: Datadog ddtrace Integration (HIGH)

**R1.1** Add `ddtrace` to `concierge_agent/supervisor_agent/requirements.txt`
- Acceptance: `ddtrace>=2.10.0` present in requirements

**R1.2** Add `ddtrace` to each MCP server's `requirements.txt` (`mcp_travel_tools/`, `mcp_cart_tools/`, `mcp_itinerary_tools/`)
- Acceptance: `ddtrace` present in all 3 MCP server requirements files

**R1.3** Modify each Dockerfile to use `ddtrace-run` as the entrypoint wrapper
- Integration point: `concierge_agent/supervisor_agent/Dockerfile` — change `CMD ["python", "agent.py"]` to `CMD ["ddtrace-run", "python", "agent.py"]`
- Same pattern for each MCP server Dockerfile
- Acceptance: All 4 Dockerfiles use `ddtrace-run`

**R1.4** Add Datadog environment variables to CDK agent-stack
- Integration point: `infrastructure/agent-stack/lib/agent-stack.ts` — add DD_* env vars to the AgentCore Runtime environment
- Variables: `DD_SERVICE`, `DD_ENV`, `DD_VERSION`, `DD_TRACE_ENABLED`, `DD_LLMOBS_ENABLED`, `DD_LLMOBS_ML_APP`, `DD_LLMOBS_AGENTLESS_ENABLED`, `DD_API_KEY`, `DD_SITE`
- Acceptance: CDK stack passes `cdk synth` with DD env vars in template

**R1.5** Add Datadog environment variables to CDK mcp-servers stack
- Integration point: `infrastructure/mcp-servers/lib/base-mcp-stack.ts`
- Acceptance: All MCP stacks inherit DD env vars

### R2: LLM Observability Spans (HIGH)

**R2.1** Auto-instrumented Bedrock LLM calls appear in Datadog LLM Observability
- Acceptance: Traces show `bedrock.invoke_model` or `bedrock.converse` spans with model_id, token counts, input/output text

**R2.2** Supervisor agent workflow appears as a parent trace
- Acceptance: Each user request creates a single trace with supervisor as root span

**R2.3** Subagent calls (travel_subagent, cart_subagent) appear as child spans
- Acceptance: Subagent spans are nested under supervisor span with `agent.type` tag

**R2.4** MCP tool calls appear as tool spans within subagent traces
- Acceptance: Tool spans show tool name, input parameters, output, and duration

### R3: APM Distributed Tracing (MEDIUM)

**R3.1** Service map shows all services: `supervisor-agent`, `travel-mcp-server`, `cart-mcp-server`, `itinerary-mcp-server`
- Acceptance: Datadog Service Map renders connected services

**R3.2** Trace context propagates across HTTP calls from agent → AgentCore Gateway → MCP servers
- Acceptance: Single trace ID spans all services

### R4: Troubleshooting Guide Documentation (HIGH)

**R4.1** Document Scenario 1: "Slow flight search" — how to identify which MCP tool call is slow using trace waterfall
- Acceptance: Step-by-step guide with expected Datadog UI navigation

**R4.2** Document Scenario 2: "High token usage" — how to find expensive prompts using LLM Observability token metrics
- Acceptance: Guide shows how to sort/filter by token count

**R4.3** Document Scenario 3: "Agent error" — how to trace an error from user-facing response back to the failing Bedrock call or tool
- Acceptance: Guide shows error propagation in trace view

### R5: Documentation & Polish (HIGH)

**R5.1** Create comprehensive README.md with architecture diagram, prerequisites, deployment steps, and troubleshooting guide
- Acceptance: README follows partner sample conventions (see existing `datadog/README.md` patterns)

**R5.2** Create architecture diagram showing data flow: User → Web UI → AgentCore Runtime (supervisor) → Gateway → MCP Servers, with Datadog Agent/agentless collection overlay
- Acceptance: Mermaid or PNG diagram in `docs/`

**R5.3** Include `.env.example` with all required environment variables documented
- Acceptance: File exists with placeholder values and comments

---

## 6. Implementation Tasks

### Phase 1: Project Scaffolding
- [ ] Create directory structure under `datadog/travel-concierge-agent-observability/`
- [ ] Copy relevant source files from upstream travel-concierge-agent (agent code, infrastructure, scripts)
- [ ] Create `.env.example` with Datadog configuration variables
- [ ] Create README.md skeleton

### Phase 2: Core Instrumentation (HIGH priority)
- [ ] Add `ddtrace` to `supervisor_agent/requirements.txt`
- [ ] Add `ddtrace` to all MCP server `requirements.txt` files
- [ ] Modify `supervisor_agent/Dockerfile` to use `ddtrace-run`
- [ ] Modify all MCP server Dockerfiles to use `ddtrace-run`
- [ ] Add `dd_instrument.py` bootstrap module for LLMObs configuration (if needed beyond env vars)
- [ ] Update CDK `agent-stack.ts` to inject DD_* environment variables
- [ ] Update CDK `base-mcp-stack.ts` to inject DD_* environment variables

### Phase 3: Validation & Manual Annotation (MEDIUM priority)
- [ ] Deploy and verify traces appear in Datadog LLM Observability
- [ ] Add manual `LLMObs` span annotations if auto-instrumentation has gaps for subagent boundaries
- [ ] Verify service map connectivity
- [ ] Verify token usage metrics are captured

### Phase 4: Documentation & Polish (HIGH priority)
- [ ] Write full README.md with deployment guide
- [ ] Create architecture diagram (Mermaid)
- [ ] Write troubleshooting scenarios (3 scenarios)
- [ ] Add screenshots/expected output descriptions
- [ ] Final review and cleanup

---

## 7. File Changes Summary

| Path | Action | Description |
|------|--------|-------------|
| `datadog/travel-concierge-agent-observability/README.md` | CREATE | Main documentation with setup, architecture, troubleshooting |
| `datadog/travel-concierge-agent-observability/.env.example` | CREATE | Template for DD_API_KEY, DD_SITE, and all DD_* env vars |
| `datadog/travel-concierge-agent-observability/docs/architecture.md` | CREATE | Mermaid architecture diagram |
| `datadog/travel-concierge-agent-observability/docs/troubleshooting-guide.md` | CREATE | 3 troubleshooting scenarios |
| `datadog/travel-concierge-agent-observability/concierge_agent/supervisor_agent/requirements.txt` | MODIFY | Add `ddtrace>=2.10.0` |
| `datadog/travel-concierge-agent-observability/concierge_agent/supervisor_agent/Dockerfile` | MODIFY | Wrap entrypoint with `ddtrace-run` |
| `datadog/travel-concierge-agent-observability/concierge_agent/supervisor_agent/agent.py` | MODIFY | Add minimal LLMObs initialization if needed |
| `datadog/travel-concierge-agent-observability/concierge_agent/mcp_travel_tools/requirements.txt` | MODIFY | Add `ddtrace>=2.10.0` |
| `datadog/travel-concierge-agent-observability/concierge_agent/mcp_travel_tools/Dockerfile` | MODIFY | Wrap entrypoint with `ddtrace-run` |
| `datadog/travel-concierge-agent-observability/concierge_agent/mcp_cart_tools/requirements.txt` | MODIFY | Add `ddtrace>=2.10.0` |
| `datadog/travel-concierge-agent-observability/concierge_agent/mcp_cart_tools/Dockerfile` | MODIFY | Wrap entrypoint with `ddtrace-run` |
| `datadog/travel-concierge-agent-observability/concierge_agent/mcp_itinerary_tools/requirements.txt` | MODIFY | Add `ddtrace>=2.10.0` |
| `datadog/travel-concierge-agent-observability/concierge_agent/mcp_itinerary_tools/Dockerfile` | MODIFY | Wrap entrypoint with `ddtrace-run` |
| `datadog/travel-concierge-agent-observability/infrastructure/agent-stack/lib/agent-stack.ts` | MODIFY | Add DD_* env vars to runtime environment |
| `datadog/travel-concierge-agent-observability/infrastructure/mcp-servers/lib/base-mcp-stack.ts` | MODIFY | Add DD_* env vars to base MCP stack |

---

## 8. Architecture

```
┌─────────────┐     ┌──────────────────────────────────────────────────────┐
│   Web UI    │────▶│  AgentCore Runtime (Supervisor Agent)                │
│  (React)    │     │  ┌─────────────────────────────────────────────────┐ │
└─────────────┘     │  │ ddtrace-run python agent.py                    │ │
                    │  │                                                 │ │
                    │  │  supervisor_agent                               │ │
                    │  │    ├── travel_subagent ──▶ BedrockModel (Claude)│ │
                    │  │    ├── cart_subagent ────▶ BedrockModel (Claude)│ │
                    │  │    └── itinerary tools (via Gateway MCP client) │ │
                    │  └─────────────────────────────────────────────────┘ │
                    └──────────────┬───────────────────────────────────────┘
                                   │ AgentCore Gateway (MCP Protocol)
                    ┌──────────────┼──────────────────────┐
                    ▼              ▼                      ▼
            ┌──────────────┐ ┌──────────────┐ ┌──────────────────┐
            │ Travel MCP   │ │  Cart MCP    │ │ Itinerary MCP    │
            │ Server       │ │  Server      │ │ Server           │
            │ (ddtrace-run)│ │ (ddtrace-run)│ │ (ddtrace-run)    │
            └──────┬───────┘ └──────┬───────┘ └──────┬───────────┘
                   │                │                 │
                   ▼                ▼                 ▼
            ┌─────────────────────────────────────────────────┐
            │              Amazon Bedrock (Claude)             │
            └─────────────────────────────────────────────────┘
                                   │
                    ┌──────────────┼──────────────────────┐
                    ▼              ▼                      ▼
            ┌──────────────────────────────────────────────────┐
            │           Datadog (Agentless)                     │
            │  ┌─────────────┐ ┌──────────┐ ┌───────────────┐ │
            │  │ LLM Observ. │ │   APM    │ │  Service Map  │ │
            │  │ Traces      │ │  Traces  │ │  Dashboard    │ │
            │  └─────────────┘ └──────────┘ └───────────────┘ │
            └──────────────────────────────────────────────────┘
```

---

## 9. Success Criteria

| # | Criterion | Verification |
|---|-----------|-------------|
| SC1 | A user query to the travel agent produces a complete trace in Datadog LLM Observability | Manual: send "Find flights from BOS to CDG" and verify trace in DD UI |
| SC2 | Trace shows supervisor → subagent → LLM call hierarchy with token counts | Manual: inspect trace waterfall in DD |
| SC3 | Service map shows all agent and MCP services connected | Manual: check DD Service Map |
| SC4 | README enables a new developer to deploy and see traces within 30 minutes (given existing AWS/DD accounts) | Manual: follow README from scratch |
| SC5 | No changes to core agent logic — only additive instrumentation | Code review: diff shows only ddtrace additions |

---

## 10. Risks & Mitigations

| # | Risk | Severity | Mitigation |
|---|------|----------|------------|
| RK1 | `ddtrace` auto-instrumentation may not fully capture Strands Agent subagent delegation boundaries | HIGH | Validate early; add manual `LLMObs.workflow()` / `LLMObs.agent()` decorators if needed |
| RK2 | AgentCore Runtime containers may not have outbound HTTPS to Datadog intake endpoints | HIGH | Use `DD_LLMOBS_AGENTLESS_ENABLED=1` for direct API submission; verify VPC/security group allows egress to `*.datadoghq.com` |
| RK3 | Trace context may not propagate through AgentCore Gateway (MCP protocol) | MEDIUM | If gateway doesn't forward trace headers, MCP server traces will be separate; document this as a known limitation and show correlation via timestamps |
| RK4 | `ddtrace` adds latency overhead to LLM calls | LOW | Overhead is typically <1ms per span; document in README |
| RK5 | Upstream travel-concierge-agent may change, breaking our fork | LOW | Pin to specific commit; document upstream source version |
| RK6 | Datadog API key management in CDK — must not be hardcoded | HIGH | Use SSM Parameter Store SecureString or Secrets Manager; document in deployment guide |

---

## 11. Dependencies

- **Upstream**: [amazon-bedrock-agentcore-samples](https://github.com/awslabs/amazon-bedrock-agentcore-samples) travel-concierge-agent (commit TBD)
- **Datadog**: `ddtrace` Python library >= 2.10.0
- **AWS**: Bedrock AgentCore access, Cognito, DynamoDB, ECR, CloudFormation
- **Datadog Account**: LLM Observability + APM enabled (trial or paid)

---

## 12. Resolved Decisions

1. **Scope of fork**: Full copy of the travel-concierge-agent (all directories) — this is a complete partner sample.
2. **Datadog Agent vs Agentless**: Agentless mode (`DD_LLMOBS_AGENTLESS_ENABLED=1`) for simplicity.
3. **Dashboard JSON export**: Rely on OOTB Datadog LLM Observability dashboards — no custom dashboard JSON.
4. **Upstream commit pinning**: Track `main` for now.
5. **Secrets Management**: Use existing Secrets Manager secrets in `datadog-member` account (`<YOUR_AWS_ACCOUNT_ID>`, `us-east-1`):
   - `datadog/aig-agent/api-key` (ARN: `arn:aws:secretsmanager:us-east-1:<YOUR_AWS_ACCOUNT_ID>:secret:datadog/aig-agent/api-key-EgB8ny`) — DD API Key
   - `datadog/aig-agent/app-key` (ARN: `arn:aws:secretsmanager:us-east-1:<YOUR_AWS_ACCOUNT_ID>:secret:datadog/aig-agent/app-key-EwJAQR`) — DD App Key
   - CDK stacks will grant Secrets Manager read access and inject secret ARNs as env vars for runtime resolution.

---

*This PRD is a DRAFT. Please review and provide feedback before implementation begins.*
