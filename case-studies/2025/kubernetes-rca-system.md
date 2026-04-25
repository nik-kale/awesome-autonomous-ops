# Case Study: Kubernetes Root Cause Analysis System

> **Anonymization Level**: Reference Architecture Example
>
> **Industry**: Technology/SaaS
>
> **Deployment Date**: Q4 2024
>
> **Last Updated**: December 2024

> ⚠️ **Note**: This is a reference architecture example, not a real company deployment. It demonstrates realistic patterns and metrics based on industry best practices.

## Executive Summary

Implemented autonomous root cause analysis system for Kubernetes incidents using LangGraph for graph-based reasoning over logs, metrics, and traces. Reduced mean time to identify (MTTI) from 30 minutes to under 5 minutes for 70% of incidents. Combined txtai for semantic log search with Prometheus metrics correlation and custom dependency graph analysis. Achieved 85% diagnostic accuracy while maintaining complete audit trails for all investigations.

## Organization Context

### Company Profile

- **Size**: 200 employees, 40 engineers
- **Scale**: 150 microservices, 50K requests/second, 500 pods across 3 clusters
- **Industry**: E-commerce SaaS platform
- **Maturity**: Growth stage (Series B)

### Pre-Implementation State

**Challenges:**
- Manual log correlation across 150 services taking 20-45 minutes per incident
- Alert fatigue with 300+ alerts per week, 40% false positives
- On-call engineers spending 60% of time on diagnostic toil
- Inconsistent incident analysis quality depending on engineer experience
- No systematic tracking of recurring failure patterns

**Existing Infrastructure:**
- **Observability**: Prometheus, Grafana, Loki (logs), Jaeger (traces)
- **Orchestration**: Kubernetes 1.27, Istio service mesh
- **Ticketing**: Jira
- **Automation**: Basic alerting rules, no automated investigation

## Goals & Success Criteria

### Primary Goals

1. **Reduce Time to Identify Root Cause**: From 30 minutes to <10 minutes
   - Target: 70% reduction in MTTI
   - Timeline: 6 months

2. **Improve Diagnostic Quality**: Consistent, high-quality analysis
   - Target: 80%+ accuracy in root cause identification
   - Timeline: Ongoing measurement

3. **Capture Organizational Knowledge**: Build searchable incident patterns
   - Target: 90% of incidents tagged with root cause categories
   - Timeline: 12 months

### Success Metrics

- **MTTI**: Reduce from 30min to <10min (achieved: 5min average)
- **Diagnostic Accuracy**: >80% (achieved: 85%)
- **Engineer Satisfaction**: >70% positive feedback (achieved: 92%)
- **False Positive Reduction**: 40% → <10% (achieved: 12%)

## Technical Architecture

### Architecture Diagram

```
┌─────────────────┐
│ Alert Manager   │
│ (Prometheus)    │
└────────┬────────┘
         │
┌────────▼──────────────────┐
│ RCA Orchestrator          │
│ (LangGraph workflow)      │
│  ┌────────────────────┐   │
│  │ 1. Alert Triage    │   │
│  │ 2. Context Gather  │   │
│  │ 3. Graph Build     │   │
│  │ 4. Root Cause ID   │   │
│  │ 5. Report Generate │   │
│  └────────────────────┘   │
└────────┬──────────────────┘
         │
┌────────▼──────────────────┐
│ Data Collection Layer     │
│                           │
│  ┌──────────────────┐    │
│  │ txtai            │    │
│  │ (log embeddings) │    │
│  └──────────────────┘    │
│                           │
│  ┌──────────────────┐    │
│  │ Prometheus       │    │
│  │ (metrics)        │    │
│  └──────────────────┘    │
│                           │
│  ┌──────────────────┐    │
│  │ Service Topology │    │
│  │ (dependency map) │    │
│  └──────────────────┘    │
└───────────────────────────┘
```

### Component Stack

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| **Agent** | Claude 3.5 Sonnet | Latest | Diagnostic reasoning |
| **RCA Engine** | LangGraph | 0.2.x | Graph-based investigation workflow |
| **Log Search** | txtai | 7.x | Semantic log search and correlation |
| **Metrics** | Prometheus | 2.45+ | Time-series metric correlation |
| **Topology** | Custom (K8s API) | N/A | Service dependency mapping |
| **Storage** | PostgreSQL | 15 | Investigation history |
| **Observability** | OpenTelemetry | 1.x | Agent performance monitoring |

### Key Design Decisions

**Decision 1: Graph-based investigation over simple prompt chain**
- **Rationale**: Kubernetes incidents require exploring multiple hypotheses, backtracking when paths don't lead to root cause, and correlating signals across logs/metrics/topology
- **Trade-offs**: More complex to implement than linear prompting, but far more effective for complex failures
- **Outcome**: 85% diagnostic accuracy vs. 45% with prompt chaining

**Decision 2: Read-only analysis, no automated remediation**
- **Rationale**: Organization preferred conservative approach to build trust before automating actions
- **Trade-offs**: Still requires human to execute fixes, but dramatically faster diagnosis
- **Outcome**: 90% engineer satisfaction, safer adoption path

**Decision 3: Semantic log search over regex patterns**
- **Rationale**: Microservices produce unstructured logs; embeddings find relevant logs even with different phrasing
- **Trade-offs**: Requires embedding pre-processing, but handles log variety much better
- **Outcome**: Found relevant logs in 95% of cases vs. 60% with regex

### Security & Governance

**Access Control:**
- RCA system has read-only access to Prometheus, Loki, Kubernetes API
- Service account with cluster-reader role
- No write permissions to any production system

**Audit & Compliance:**
- All LLM API calls logged with input/output
- Investigation history stored for 90 days
- Engineer approval required before viewing PII-containing logs

## Implementation Journey

### Phase 1: Proof of Concept (2 weeks)

**Scope**:
- Single namespace (non-production staging environment)
- Manual trigger only (no automated alerts)
- Focused on OOMKilled and CrashLoopBackOff scenarios

**Team**: 1 SRE, 1 ML engineer (50% time)

**Results**:
- Successfully identified root cause in 4/5 test incidents
- Reduced investigation time from 25min to 8min (average)
- Decision to proceed with pilot

### Phase 2: Pilot Deployment (6 weeks)

**Scope**:
- Production cluster (non-critical services only)
- Automated trigger on high-severity alerts
- Expanded to cover pod failures, deployment issues, resource exhaustion

**Challenges**:

1. **Challenge: Too many irrelevant logs retrieved**
   - **Solution**: Implemented time-window narrowing (alert time ± 10min) and service-specific filtering
   - **Outcome**: Reduced log noise by 75%

2. **Challenge: Dependency graph incomplete for external services**
   - **Solution**: Manual annotation of external dependencies, automated discovery for internal services
   - **Outcome**: 95% topology coverage

3. **Challenge: LLM occasionally hallucinated metrics that didn't exist**
   - **Solution**: Constrained agent to only query metrics that exist in Prometheus schema, validation layer
   - **Outcome**: Hallucination rate reduced to <3%

### Phase 3: Production Rollout (3 months)

**Rollout Strategy**: Service-by-service, starting with highest-incident services

**Adoption Metrics**:
- Week 1: 10% of services (highest-priority)
- Month 1: 40% of services
- Month 3: 100% of services

**User Adoption**:
- 92% of on-call engineers actively using RCA reports
- 78% report trusting the analysis "most of the time"

## Results & Impact

### Quantitative Results

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **MTTI** | 30 min | 5 min | 83% reduction |
| **Incidents with RCA** | 20% | 90% | 350% increase |
| **Diagnostic Accuracy** | N/A | 85% | N/A |
| **Engineering Time Saved** | N/A | 25 hrs/week | N/A |
| **False Positive Alerts Acted On** | 40% | 12% | 70% reduction |

### Qualitative Impact

**Team Experience:**
- "I can now handle incidents in services I've never worked on" - Senior SRE
- "The dependency graph visualization alone is worth it" - Platform Engineer
- "Freed me up to actually fix issues instead of hunting for them" - On-call Engineer

**Organizational Benefits:**
- SRE team redirected 30% of time from diagnostics to proactive reliability work
- Standardized incident analysis format improved team handoffs
- Built searchable knowledge base of failure patterns

**Unexpected Wins:**
- RCA reports became onboarding material for new engineers
- Identified 3 persistent issues that were previously masked by symptoms
- Improved Prometheus query optimization through analysis of common patterns

## Challenges & Solutions

### Challenge 1: Token cost explosion with verbose logs

**Problem**: Initial implementation sent entire log dumps to LLM, costing $50/day for medium-traffic period

**Attempted Solutions**:
1. Log sampling (10% of logs) - Missed critical errors
2. Regex pre-filtering - Too brittle for varied log formats

**Final Solution**: Two-stage approach
- Stage 1: txtai semantic search retrieves top 50 relevant log lines
- Stage 2: LLM analyzes only those lines with surrounding context

**Lessons**: Semantic pre-filtering is essential for cost-effective LLM investigation

---

### Challenge 2: Circular dependencies in service graph confused reasoning

**Problem**: Agent got stuck in loops when investigating services that had bidirectional dependencies

**Attempted Solutions**:
1. Graph traversal limits (max depth 5) - Missed some root causes
2. Simple cycle detection - Too aggressive, pruned valid paths

**Final Solution**: LangGraph state management with visited-node tracking and hypothesis scoring

**Lessons**: Graph-based workflows need explicit cycle handling and backtracking logic

---

### Challenge 3: Engineers skeptical of "AI magic"

**Problem**: Initial rollout faced pushback: "How do I know it's right?"

**Attempted Solutions**:
1. Showing confidence scores - Engineers ignored them
2. Detailed technical explanations - Too verbose

**Final Solution**: 
- Show evidence chain: "Found ERROR in service X → correlated with spike in metric Y → dependency on failing service Z"
- Allow engineers to drill into each step
- Mark analysis as "high confidence" vs. "needs verification"

**Lessons**: Explainability is critical for adoption. Show your work, don't just give answers.

## Lessons Learned

### What Worked Well

1. **Graph-based reasoning**: LangGraph's ability to explore hypotheses, backtrack, and synthesize findings dramatically outperformed linear chains
2. **Read-only first**: Building trust with diagnostic-only system enabled future automation
3. **Semantic search**: txtai embeddings handled log variety far better than regex patterns
4. **Explicit evidence chains**: Showing reasoning steps built engineer confidence

### What We'd Do Differently

1. **Start with dependency graph**: We built this late; should have been foundation from day 1
2. **Invest in eval framework earlier**: Took 4 weeks to build proper accuracy measurement; should have been parallel to development
3. **Limit scope of POC more aggressively**: Tried to handle too many incident types initially; focus on 1-2 patterns first

### Surprises & Unexpected Findings

- **Finding 1**: Engineers valued the structured investigation format (JSON schema) as much as the actual root cause - made handoffs easier
- **Finding 2**: System found more instances of "known issues" (like memory leaks) that were previously missed due to investigation fatigue

## Recommendations for Others

### For Similar Organizations

**If you're running Kubernetes at scale (50+ services):**
- ✅ **Do**: Start with read-only diagnostic system before automating remediation
- ✅ **Do**: Invest in semantic log search; regex won't scale
- ✅ **Do**: Build explicit dependency graph; critical for accurate analysis
- ❌ **Don't**: Send raw logs to LLM; use retrieval to filter first
- ❌ **Don't**: Skip the explainability layer; engineers need to verify reasoning

### Prerequisites

Before attempting this implementation, ensure you have:

- [x] Centralized logging (Loki, Elasticsearch, etc.)
- [x] Prometheus or equivalent metrics system
- [x] Service dependency map (or ability to discover it)
- [x] Kubernetes cluster with stable observability
- [x] At least 3 months of historical incident data for evaluation

### Estimated Resources

**Time**: 3-4 months with 1.5 FTE engineers (1 SRE + 0.5 ML engineer)

**Budget**: 
- Infrastructure: $500/month (embedding storage, PostgreSQL, compute)
- LLM API: $300-800/month depending on incident volume
- Development: ~$100K in engineering time

**Team**: 1 SRE (Kubernetes expert), 0.5 ML engineer (LLM/embeddings), 0.25 product manager

## Future Plans

### Short-Term (Next 3-6 months)

- Expand to cover network issues (current focus: pod/deployment failures)
- Add automated ticket creation with RCA report attached
- Integrate with Slack for conversational follow-up questions

### Long-Term (Next 12 months)

- Pilot automated remediation for safe, well-understood failure modes (e.g., pod restarts)
- Multi-cluster analysis (currently single-cluster only)
- Predictive incident detection using pattern recognition

## Appendix

### Sample LangGraph Workflow

```python
# Simplified LangGraph investigation workflow
from langgraph.graph import StateGraph

class InvestigationState(TypedDict):
    alert: Alert
    metrics: List[MetricSeries]
    logs: List[LogEntry]
    topology: ServiceGraph
    hypotheses: List[Hypothesis]
    root_cause: Optional[RootCause]

workflow = StateGraph(InvestigationState)

workflow.add_node("triage", triage_alert)
workflow.add_node("gather_metrics", fetch_related_metrics)
workflow.add_node("search_logs", semantic_log_search)
workflow.add_node("analyze", llm_analysis)
workflow.add_node("verify", verify_hypothesis)

workflow.set_entry_point("triage")
workflow.add_conditional_edges("verify", should_continue_investigating)
```

### Sample txtai Log Query

```python
# Semantic search for relevant logs given an alert
import txtai

index = txtai.Embeddings()
index.load("logs-embeddings-index")

query = f"error related to {alert.service} around {alert.timestamp}"
results = index.search(query, limit=50)

# Returns log entries semantically similar to query
```

### References

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [txtai Embeddings Guide](https://neuml.github.io/txtai/)
- [Kubernetes Troubleshooting Best Practices](https://kubernetes.io/docs/tasks/debug/)

---

## Contact

**Author**: Reference Architecture Example

**Organization**: N/A - Educational Template

**Questions?**: Please open an issue in the [awesome-autonomous-ops repository](https://github.com/nik-kale/awesome-autonomous-ops/issues)

---

**Last updated**: December 2024

**Version**: 1.0

