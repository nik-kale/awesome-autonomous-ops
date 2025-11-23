# Glossary of Autonomous Operations Terms

A comprehensive reference for terminology used in AI-powered autonomous operations, SRE, and DevOps.

## Core Concepts

### Autonomous Operations
The use of AI agents to independently perform operational tasks including incident diagnosis, remediation, and infrastructure management with minimal human intervention. Distinct from traditional automation in that agents can reason, adapt, and handle novel scenarios.

### Agentic System
A software system that can perceive its environment, make decisions, and take actions to achieve goals. In ops context: agents that monitor systems, investigate alerts, and execute remediation workflows.

### Human-in-the-Loop (HITL)
A safety pattern where critical actions require human approval before execution. Common in autonomous ops for write operations (deployments, config changes, restarts).

## AI & LLM Concepts

### Retrieval-Augmented Generation (RAG)
An AI pattern that combines:
1. **Retrieval**: Finding relevant context from documents/logs/metrics
2. **Augmentation**: Providing context to the LLM
3. **Generation**: LLM produces answers grounded in retrieved data

Used in ops for answering questions based on runbooks, logs, and incident history.

### Graph RAG
An advanced RAG approach that:
- Constructs knowledge graphs from operational data
- Uses graph traversal for multi-hop reasoning
- Correlates entities across logs, metrics, traces, and config

Superior to traditional RAG for root cause analysis because it preserves relationships between entities (services, hosts, dependencies).

### Embedding
A vector representation of text/data. In ops:
- Log lines → embeddings for semantic search
- Runbook sections → embeddings for retrieval
- Alert descriptions → embeddings for similarity matching

### Semantic Search
Search based on meaning rather than keywords. Example: Searching for "pods crashing" also finds "containers terminating unexpectedly."

### Tool Use / Function Calling
LLM capability to invoke external functions/APIs. In ops:
- Query Prometheus metrics
- Create Jira tickets
- Restart Kubernetes pods
- Search documentation

### Model Context Protocol (MCP)
An open protocol (by Anthropic) for connecting AI agents to data sources and tools. Standardizes how LLMs access external systems like GitHub, Prometheus, Kubernetes, etc.

**MCP Server**: A service that exposes tools/resources to AI via MCP protocol.
**MCP Gateway**: A security layer that enforces policies, approvals, and audit logging for MCP interactions.

## Observability & Reliability

### SRE (Site Reliability Engineering)
Google's approach to operations focusing on:
- Service Level Objectives (SLOs)
- Error budgets
- Automation over manual toil
- Blameless postmortems

Autonomous ops is the evolution of SRE principles using AI.

### DevOps
Cultural movement emphasizing:
- Collaboration between development and operations
- Continuous integration/deployment (CI/CD)
- Infrastructure as Code (IaC)
- Shared responsibility for reliability

### SecOps
Security operations: monitoring, threat detection, incident response. Autonomous SecOps uses AI for threat hunting and automated remediation.

### MTTR (Mean Time To Resolve)
Average time from incident detection to resolution. Key metric for measuring autonomous ops impact.

### MTTD (Mean Time To Detect)
Average time from incident occurrence to detection. AI can reduce MTTD via anomaly detection.

### MTTI (Mean Time To Investigate)
Time spent diagnosing root cause. Graph RAG and agentic systems target MTTI reduction.

### Toil
Repetitive, manual, automatable operational work. Autonomous ops aims to eliminate toil via intelligent automation.

### Runbook
Step-by-step instructions for handling operational scenarios (deployments, incidents, maintenance). Autonomous agents can execute runbooks automatically.

### Playbook
Collection of runbooks organized by domain (Kubernetes, database, networking). Used as knowledge base for AI agents.

### Root Cause Analysis (RCA)
Process of identifying the underlying cause of an incident. Agentic RCA uses graph reasoning and multi-signal correlation.

## Incident Management

### Alert
Notification that a metric has crossed a threshold or anomaly detected. Triggers investigation.

### Incident
An unplanned disruption or degradation of service requiring response.

### Severity Levels
- **P0/SEV1**: Critical - Total outage, immediate response
- **P1/SEV2**: High - Significant degradation, rapid response
- **P2/SEV3**: Medium - Minor impact, normal response
- **P3/SEV4**: Low - Minimal impact, can be scheduled

### On-Call
Engineers responsible for responding to alerts outside business hours. Autonomous ops can reduce on-call burden.

### War Room
Virtual space where engineers collaborate during major incidents. Modern war rooms include AI agents as participants.

### Postmortem
Blameless analysis after incident resolution documenting:
- Timeline
- Root cause
- Impact
- Action items

AI can generate postmortems from incident data.

## Remediation & Automation

### Auto-Remediation
Automated actions to resolve incidents without human intervention. Examples:
- Restart failed pods
- Scale up resources
- Clear cache
- Rollback deployment

### Circuit Breaker
Safety pattern that stops automated actions if failure rate exceeds threshold. Prevents automation from making incidents worse.

### Chaos Engineering
Deliberately injecting failures to test system resilience. Used to train and validate autonomous remediation agents.

### Canary Deployment
Gradual rollout to subset of users before full deployment. AI can monitor canary metrics and auto-rollback if issues detected.

### Blue-Green Deployment
Maintaining two identical environments. AI can orchestrate traffic switching and rollback.

## Browser & Desktop Automation

### Headless Browser
Browser without GUI, controlled programmatically. Used by ops agents to interact with dashboards and consoles.

### Playwright / Selenium
Browser automation frameworks. Enable AI agents to navigate web UIs that lack APIs.

### Computer Vision for Ops
Using AI vision models to "read" dashboards and consoles. Useful when scraping HTML isn't reliable.

### Screen Scraping
Extracting data from UI. Less reliable than APIs but necessary for legacy systems.

## Compliance & Governance

### Policy as Code
Expressing governance policies as executable code. Used with tools like Open Policy Agent (OPA) to constrain agent behavior.

### Audit Trail / Audit Log
Record of all agent actions (who, what, when, why). Critical for compliance and security.

### Blast Radius
Scope of potential damage from an automated action. Governance policies limit blast radius (e.g., affect only one pod, not entire deployment).

### Approval Workflow
Multi-step process requiring human approval for sensitive operations. Common in production autonomous ops.

### RBAC (Role-Based Access Control)
Defining what actions agents can perform based on assigned roles. More granular than allowing full access.

### Compliance Frameworks
- **SOC 2**: Security and availability controls
- **GDPR**: Data privacy regulations
- **HIPAA**: Healthcare data protection
- **PCI DSS**: Payment card data security

Autonomous ops systems must comply with relevant frameworks.

## Data Sources

### Logs
Time-series text records of events. Sources: applications, infrastructure, security. Used for investigation and RCA.

### Metrics
Numerical measurements over time (CPU, latency, error rate). Stored in time-series databases like Prometheus.

### Traces
Records of request flow through distributed systems. Enable understanding of cross-service dependencies.

### Configuration Changes
Modifications to infrastructure, code, or settings. Often correlate with incidents.

### Dependency Graph
Map of service dependencies. Critical for blast radius analysis and RCA.

## Platforms & Tools

### Kubernetes / K8s
Container orchestration platform. Common target for autonomous ops (auto-scaling, self-healing).

### Prometheus
Open-source metrics and alerting system. De facto standard for Kubernetes monitoring.

### Grafana
Visualization platform for metrics and logs. Agents can read Grafana dashboards via browser automation.

### Splunk
Enterprise log aggregation and analysis platform.

### ELK Stack
Elasticsearch, Logstash, Kibana. Open-source log management.

### Jaeger / Tempo
Distributed tracing platforms.

### PagerDuty / Opsgenie
Incident alerting and on-call management.

### Jira / ServiceNow
Ticketing systems for incident tracking.

### Terraform
Infrastructure as Code tool. Agents can analyze Terraform for config changes.

## Safety & Testing

### Sandbox Environment
Isolated environment for testing agent behavior before production deployment.

### Dry Run Mode
Agent simulates actions without executing them. Used for validation.

### Rollback
Reverting to previous known-good state after failed change.

### Idempotency
Property where repeated executions produce same result. Critical for safe remediation (running twice doesn't cause double-scaling).

### Rate Limiting
Restricting number of actions per time period. Prevents runaway automation.

## Performance & Efficiency

### Token
Unit of text processed by LLMs. Roughly 4 characters. Impacts cost and latency.

### Prompt Engineering
Crafting prompts to get desired behavior from LLMs. Critical for accurate diagnostics.

### Caching
Storing LLM responses for reuse. Reduces cost for repeated queries.

### Batch Processing
Processing multiple items together. More efficient than one-by-one for log analysis.

## Ecosystem Terms

### Awesome List
Curated collection of resources on a topic. This repository is an "awesome list" for autonomous ops.

### OSI-Approved License
Open source license recognized by Open Source Initiative (MIT, Apache 2.0, GPL, etc.).

### Community-Driven
Project where community contributes features, documentation, and governance. Contrasts with vendor-controlled.

### Production-Ready
Software that meets quality bar for use in production environments (tested, documented, supported).

### Reference Implementation
Example implementation demonstrating best practices. Used as template for custom deployments.

### Reference Architecture
Diagram and documentation showing how components fit together. Helps with design decisions.

---

## Related Resources

- [GETTING-STARTED.md](./GETTING-STARTED.md) - Practical guide to building autonomous ops systems
- [ARCHITECTURES.md](./ARCHITECTURES.md) - Reference architectures and design patterns
- [COMPARISONS.md](./COMPARISONS.md) - Tool comparison matrices

## Contributing

Missing a term? Found an error? Please [open an issue](https://github.com/nik-kale/awesome-autonomous-ops/issues/new/choose) or submit a PR to improve this glossary.

---

Last updated: 2025-11-23
