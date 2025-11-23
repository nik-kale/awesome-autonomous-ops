# Reference Architectures for Autonomous Operations

Proven architectural patterns and complete stack examples for building production-grade autonomous operations systems.

## Table of Contents

- [Foundational Principles](#foundational-principles)
- [Architecture 1: Read-Only Investigation Assistant](#architecture-1-read-only-investigation-assistant)
- [Architecture 2: HITL Remediation System](#architecture-2-hitl-remediation-system)
- [Architecture 3: Full Autonomous Platform](#architecture-3-full-autonomous-platform)
- [Cross-Cutting Concerns](#cross-cutting-concerns)
- [Deployment Patterns](#deployment-patterns)
- [Security Boundaries](#security-boundaries)

---

## Foundational Principles

### Design Philosophy

1. **Defense in Depth**: Multiple security layers (RBAC, policies, approval workflows, circuit breakers)
2. **Observability First**: Instrument everything - agent actions, LLM calls, tool invocations
3. **Progressive Trust**: Start read-only, add write access gradually with proven safety
4. **Blast Radius Limits**: Constrain scope of automated actions (one pod before entire deployment)
5. **Human Override**: Always allow humans to take control and override agent decisions

### Component Categories

Every autonomous ops architecture includes:

- **Diagnostic Layer**: RCA, log analysis, metric correlation
- **Tool Access Layer**: MCP servers, browser automation, API clients
- **Orchestration Layer**: Workflow engine, agent coordination
- **Safety Layer**: Policy enforcement, approval workflows, circuit breakers
- **Observability Layer**: Logging, metrics, traces for agent behavior

---

## Architecture 1: Read-Only Investigation Assistant

**Goal**: Accelerate incident investigation without automation risk
**Maturity**: Production-ready for all environments
**Timeline**: 2-4 weeks to deploy

### Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         Engineer UI (Slack/Web)                  │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                    Investigation Agent (LLM)                     │
│  - Receives alerts and questions                                 │
│  - Plans diagnostic steps                                        │
│  - Generates hypotheses                                          │
│  - Synthesizes findings                                          │
└─────────┬────────────────────────────────────┬──────────────────┘
          │                                    │
          │ (Read-Only MCP Calls)              │
          │                                    │
┌─────────▼─────────────┐          ┌──────────▼──────────────────┐
│   MCP Server Cluster  │          │  Browser Automation Agent   │
│                       │          │  (Playwright)               │
│ ┌───────────────────┐ │          │                             │
│ │ Prometheus Server │ │          │ - Grafana dashboards        │
│ └───────────────────┘ │          │ - Splunk queries            │
│ ┌───────────────────┐ │          │ - Custom consoles           │
│ │ GitHub Server     │ │          └─────────────────────────────┘
│ └───────────────────┘ │
│ ┌───────────────────┐ │
│ │ K8s Server        │ │
│ └───────────────────┘ │
│ ┌───────────────────┐ │
│ │ Jira Server       │ │
│ └───────────────────┘ │
└───────────────────────┘
          │
┌─────────▼─────────────────────────────────────────────┐
│              Observability Platforms                   │
│  - Prometheus (metrics)                                │
│  - Loki (logs)                                         │
│  - Jaeger (traces)                                     │
│  - Kubernetes API (state)                              │
└────────────────────────────────────────────────────────┘
```

### Component Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Agent** | Claude 3.5 Sonnet + LangGraph | Diagnostic reasoning |
| **MCP Servers** | Official MCP servers | Safe read access to tools |
| **Browser Automation** | Playwright | Dashboard access (read-only) |
| **Observability** | Prometheus + Loki + Jaeger | Data sources |
| **UI** | Slack bot or web interface | Engineer interaction |

### Key Features

- ✅ **Zero production risk**: Read-only access to all systems
- ✅ **Fast deployment**: No security approvals needed for read-only
- ✅ **High ROI**: Reduces MTTI by 40-60% in typical deployments
- ✅ **Learning mode**: Builds confidence before adding write access

### Example Workflow

1. **Alert triggered**: High error rate on `checkout-service`
2. **Engineer asks**: "What's causing the checkout errors?"
3. **Agent investigates**:
   - Queries Prometheus for error rate trend
   - Checks K8s pod status and recent restarts
   - Searches logs for stack traces
   - Reviews recent deploys in GitHub
   - Examines dependency graph
4. **Agent responds**: "Root cause: Database connection pool exhausted. Correlation with deployment 2h ago that increased traffic by 40%. Recommendation: Scale DB connections or add rate limiting."
5. **Engineer takes action**: Manual remediation with agent guidance

### Deployment Guide

```yaml
# kubernetes deployment (simplified)
apiVersion: apps/v1
kind: Deployment
metadata:
  name: investigation-agent
spec:
  template:
    spec:
      containers:
      - name: agent
        image: investigation-agent:latest
        env:
        - name: ANTHROPIC_API_KEY
          valueFrom:
            secretKeyRef:
              name: anthropic-secret
              key: api-key
        - name: MODE
          value: "READ_ONLY"
        volumeMounts:
        - name: mcp-config
          mountPath: /config/mcp
      volumes:
      - name: mcp-config
        configMap:
          name: mcp-servers-config
```

---

## Architecture 2: HITL Remediation System

**Goal**: Automated remediation with human approval
**Maturity**: Production-ready with proper safety controls
**Timeline**: 1-2 months to deploy

### Architecture Diagram

```
┌──────────────────────────────────────────────────────────────┐
│                  Engineer UI + Approval Portal                │
└────────┬──────────────────────────────┬────────────────────────┘
         │                              │
         │ Approval                     │ Status/Logs
         │                              │
┌────────▼──────────────────────────────▼───────────────────────┐
│                  Orchestration Engine                          │
│  - Receives incidents                                          │
│  - Plans remediation                                           │
│  - Requests approvals for write ops                            │
│  - Executes approved actions                                   │
│  - Monitors outcomes                                           │
└─────────┬────────────────────────────┬────────────────────────┘
          │                            │
          │ (via Secure Gateway)       │
          │                            │
┌─────────▼────────────────┐    ┌─────▼──────────────────────┐
│ Secure MCP Gateway       │    │  Remediation Executor      │
│                          │    │  (StackStorm/Rundeck)      │
│ - Policy enforcement     │    │                            │
│ - RBAC checks            │    │ - Runbook execution        │
│ - Approval workflows     │    │ - State management         │
│ - Audit logging          │    │ - Rollback capability      │
│ - Rate limiting          │    └────────────────────────────┘
│                          │
│ Allowed Operations:      │
│ ✅ Restart pods          │
│ ✅ Scale replicas        │
│ ✅ Clear cache           │
│ ✅ Rollback deployment   │
│ ❌ Delete resources      │
│ ❌ Modify secrets        │
└──────────┬───────────────┘
           │
┌──────────▼──────────────────────────────────────┐
│        Production Infrastructure                 │
│  - Kubernetes clusters                           │
│  - Databases                                     │
│  - Caches                                        │
│  - Load balancers                                │
└──────────────────────────────────────────────────┘
```

### Component Stack

| Layer | Technology | Purpose |
|-------|------------|---------|
| **Agent** | Claude 3.5 Sonnet + AutoRCA-Core | Diagnosis + remediation planning |
| **Gateway** | Secure-MCP-Gateway | Policy enforcement + approvals |
| **Executor** | StackStorm or Rundeck | Runbook execution |
| **Approval UI** | Slack + web portal | Human-in-the-loop |
| **Audit** | Elasticsearch + Kibana | Compliance logging |

### Safety Controls

```yaml
# Example OPA policy for agent actions
package autonomous_ops

# Allow pod restarts
allow {
    input.action == "restart_pod"
    input.blast_radius <= 1  # Only one pod
    input.severity >= "P2"    # Medium or higher
    input.approved == true    # Human approved
}

# Allow scaling (with limits)
allow {
    input.action == "scale_replicas"
    input.new_replicas <= input.current_replicas * 2  # Max 2x scale
    input.approved == true
}

# Deny dangerous operations
deny {
    input.action == "delete_deployment"
}

deny {
    input.action == "modify_secret"
}
```

### Example Workflow

1. **Incident detected**: Pod crash loop in production
2. **Agent diagnoses**: OOMKilled due to memory leak in recent deployment
3. **Agent proposes**: "Rollback to version 1.2.3 and restart affected pods"
4. **Agent requests approval**:
   ```
   🚨 Remediation Approval Required

   Incident: checkout-service crash loop
   Root Cause: Memory leak in v1.2.4
   Proposed Actions:
   1. Rollback deployment to v1.2.3 (last known good)
   2. Restart 3 affected pods
   3. Monitor error rate for 10 minutes

   Blast Radius: 3 pods (25% of replicas)
   Risk Level: Low
   Estimated Time: 5 minutes

   [Approve] [Reject] [Modify]
   ```
5. **Engineer approves**: Click "Approve" in Slack
6. **Agent executes**: Via Secure-MCP-Gateway
7. **Agent monitors**: Confirms error rate drops, incident resolved

### Approval Workflow Tiers

**Tier 1: Auto-Approve (no human needed)**
- Read operations
- Log queries
- Metric collection
- Status checks

**Tier 2: Single Approval (SRE on-call)**
- Restart pods
- Scale replicas (within limits)
- Clear caches
- Rollback deployments

**Tier 3: Dual Approval (SRE + Manager)**
- Large-scale changes (>50% of replicas)
- Database modifications
- Security-sensitive operations
- Cross-service changes

**Tier 4: Prohibited (always denied)**
- Delete production resources
- Modify secrets/credentials
- Disable security controls
- Cross-region operations

---

## Architecture 3: Full Autonomous Platform

**Goal**: Minimal human intervention for routine incidents
**Maturity**: Advanced - requires proven safety track record
**Timeline**: 3-6 months to deploy

### Architecture Diagram

```
┌────────────────────────────────────────────────────────────────┐
│                    Autonomous Ops Platform                      │
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐ │
│  │  Alert       │  │ Multi-Agent  │  │  Remediation         │ │
│  │  Ingestion   │──▶ Coordination │──▶ Orchestration        │ │
│  └──────────────┘  └──────────────┘  └──────────────────────┘ │
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │             Graph RAG Knowledge Base                      │  │
│  │  - Incident history    - Dependency graphs                │  │
│  │  - Runbook corpus      - Config changes                   │  │
│  └──────────────────────────────────────────────────────────┘  │
└──────────────┬──────────────────────────────┬──────────────────┘
               │                              │
               │                              │
┌──────────────▼─────────────┐  ┌────────────▼──────────────────┐
│   Governance Layer         │  │   Continuous Learning          │
│                            │  │                                │
│ - OPA policies             │  │ - Success rate tracking        │
│ - Circuit breakers         │  │ - Failure analysis             │
│ - Rate limiters            │  │ - Runbook optimization         │
│ - Anomaly detection (Falco)│  │ - Fine-tuning prompts          │
└────────────┬───────────────┘  └───────────────────────────────┘
             │
┌────────────▼───────────────────────────────────────────────────┐
│                  Execution Layer (Secure Gateway)               │
│                                                                 │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │
│  │ K8s API  │  │ Cloud    │  │ Ticket   │  │ Observability│   │
│  │          │  │ Provider │  │ Systems  │  │ Platforms    │   │
│  └──────────┘  └──────────┘  └──────────┘  └──────────────┘   │
└────────────────────────────────────────────────────────────────┘
```

### Key Differences from Architecture 2

**Autonomous Decision Making:**
- Pre-approved action categories don't need human confirmation
- Circuit breakers automatically pause if error rate increases
- Multi-agent coordination for complex incidents
- Continuous learning from successes and failures

**Advanced Safety:**
```python
class CircuitBreaker:
    """Prevents runaway automation."""

    def __init__(self, error_threshold=0.1, time_window=3600):
        self.error_threshold = error_threshold
        self.time_window = time_window
        self.recent_actions = []

    def can_execute(self, action_type):
        # Calculate recent error rate
        recent = self._get_recent_actions(self.time_window)
        if not recent:
            return True

        errors = sum(1 for a in recent if a['status'] == 'failed')
        error_rate = errors / len(recent)

        if error_rate > self.error_threshold:
            self._alert_humans(f"Circuit breaker open: {error_rate:.1%} error rate")
            return False

        return True
```

### Pre-Approved Action Categories

After 90 days of successful HITL operation with <5% error rate:

**Auto-Approved (no confirmation needed):**
- Restart single crashed pod
- Scale replicas ±20% within min/max bounds
- Clear application caches
- Rollback deployment to last known good (if <30min old)

**Still Require Approval:**
- Multi-pod restarts (>3 pods)
- Large-scale scaling (>50% change)
- Cross-service changes
- Database operations

### Multi-Agent Coordination

Complex incidents may involve multiple specialized agents:

```
Incident: E-commerce checkout flow degraded

┌─────────────────┐
│ Coordinator     │ ◄─── Receives alert
│ Agent           │
└────────┬────────┘
         │
         ├──────┐
         │      │
    ┌────▼───┐  ┌────▼──────┐
    │ Front  │  │ Backend   │
    │ End    │  │ Services  │
    │ Agent  │  │ Agent     │
    └────┬───┘  └────┬──────┘
         │           │
         │      ┌────▼──────┐
         │      │ Database  │
         │      │ Agent     │
         │      └────┬──────┘
         │           │
    ┌────▼───────────▼───┐
    │ Root Cause         │ ◄─── Synthesizes findings
    │ Synthesis Agent    │
    └────┬───────────────┘
         │
    ┌────▼───────────────┐
    │ Remediation        │ ◄─── Plans and executes fix
    │ Agent              │
    └────────────────────┘
```

Each agent has domain expertise (frontend, database, networking) and they collaborate to solve complex issues.

---

## Cross-Cutting Concerns

### Observability for Agents

Instrument agent behavior as rigorously as production services:

**Metrics to Track:**
- Agent invocations per hour
- LLM tokens consumed (cost tracking)
- Tool call latency
- Remediation success rate
- Human override rate
- False positive rate

**Logging:**
```json
{
  "timestamp": "2025-11-23T10:15:30Z",
  "agent_id": "rca-agent-01",
  "incident_id": "INC-12345",
  "action": "query_prometheus",
  "query": "rate(http_errors[5m])",
  "result_size_kb": 23,
  "latency_ms": 450,
  "cost_tokens": 1200
}
```

**Dashboards:**
- Agent performance dashboard (Grafana)
- Cost tracking ($/incident)
- MTTR comparison (with vs without agent)

### Cost Optimization

**Token Usage Strategies:**

1. **Use smaller models for classification:**
   ```python
   # Use Haiku for simple tasks
   if task_complexity == "low":
       model = "claude-3-haiku"  # Cheaper
   else:
       model = "claude-3-5-sonnet"  # More capable
   ```

2. **Cache common queries:**
   ```python
   # Cache runbook retrievals
   @lru_cache(maxsize=100)
   def get_runbook(service_name):
       return retrieve_from_vector_db(service_name)
   ```

3. **Batch log analysis:**
   ```python
   # Analyze logs in batches, not one-by-one
   logs = get_recent_logs(service, limit=100)
   summary = analyze_logs_batch(logs)  # Single LLM call
   ```

**Estimated Costs (100 incidents/month):**
- **Architecture 1** (Read-only): ~$200/month
- **Architecture 2** (HITL): ~$500/month
- **Architecture 3** (Full auto): ~$1500/month

### Data Flow & Security Boundaries

```
┌─────────────────────────────────────────────────────────────┐
│                      DMZ / Edge                              │
│  - TLS termination                                           │
│  - Authentication (OAuth, SAML)                              │
│  - Rate limiting                                             │
└───────────────────────┬─────────────────────────────────────┘
                        │ (Encrypted)
┌───────────────────────▼─────────────────────────────────────┐
│                  Agent Control Plane                         │
│  - Request validation                                        │
│  - Policy evaluation (OPA)                                   │
│  - Audit logging                                             │
└───────────────────────┬─────────────────────────────────────┘
                        │ (mTLS)
┌───────────────────────▼─────────────────────────────────────┐
│                  Execution Plane                             │
│  - Tool invocation                                           │
│  - Result collection                                         │
│  - Rollback on failure                                       │
└───────────────────────┬─────────────────────────────────────┘
                        │ (Service mesh)
┌───────────────────────▼─────────────────────────────────────┐
│              Production Infrastructure                       │
│  - Kubernetes clusters                                       │
│  - Databases                                                 │
│  - External services                                         │
└──────────────────────────────────────────────────────────────┘
```

**Security Controls at Each Layer:**

1. **DMZ**: Block malicious requests, enforce authentication
2. **Control Plane**: Evaluate policies, require approvals, log all actions
3. **Execution Plane**: Enforce least privilege, use service accounts
4. **Infrastructure**: RBAC, network policies, secrets management

---

## Deployment Patterns

### Pattern 1: Sidecar Deployment

Deploy agent as sidecar to existing services:

```yaml
spec:
  containers:
  - name: app
    image: myapp:latest
  - name: ops-agent
    image: ops-agent:latest
    env:
    - name: MONITOR_SERVICE
      value: "myapp"
```

**Pros**: Tightly coupled, low latency
**Cons**: Resource overhead per service

### Pattern 2: Centralized Platform

Single agent cluster serving all services:

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: autonomous-ops-platform
spec:
  replicas: 3  # HA
  template:
    spec:
      containers:
      - name: platform
        image: ops-platform:latest
```

**Pros**: Efficient resource usage, easier updates
**Cons**: Single point of failure (requires HA)

### Pattern 3: Hybrid

Lightweight agents per service + centralized coordinator:

**Best of both worlds**: Local context awareness + central knowledge

---

## Security Boundaries

### Network Segmentation

```
┌──────────────────┐
│  Agent Network   │  (Restricted)
└────────┬─────────┘
         │
         ├──── Can access: Observability platforms (read)
         ├──── Can access: Ticketing systems (read/write)
         ├──── Can access: K8s API (via gateway, restricted)
         │
         ├──── Cannot access: Databases directly
         ├──── Cannot access: Secrets stores directly
         └──── Cannot access: Production traffic
```

### Least Privilege

```yaml
# Kubernetes ServiceAccount for agent
apiVersion: v1
kind: ServiceAccount
metadata:
  name: ops-agent
---
apiVersion: rbac.authorization.k8s.io/v1
kind: Role
metadata:
  name: ops-agent-role
rules:
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["get", "list", "watch"]
- apiGroups: [""]
  resources: ["pods"]
  verbs: ["delete"]  # Only for approved restarts
  resourceNames: []  # Populated dynamically by gateway
```

---

## Next Steps

**Choosing Your Architecture:**

1. **Start with Architecture 1** (read-only) for all environments
2. **Graduate to Architecture 2** (HITL) after 30 days and >80% diagnostic accuracy
3. **Consider Architecture 3** (full auto) only after 90 days of HITL with <5% error rate

**Resources:**
- [GETTING-STARTED.md](./GETTING-STARTED.md) - Implementation guide
- [COMPARISONS.md](./COMPARISONS.md) - Tool selection
- [SECURITY.md](./SECURITY.md) - Security best practices

---

Last updated: 2025-11-23
