# Case Study: Human-in-the-Loop Remediation System

> **Anonymization Level**: Reference Architecture Example
>
> **Industry**: Healthcare Technology
>
> **Deployment Date**: Q3 2024
>
> **Last Updated**: December 2024

> ⚠️ **Note**: This is a reference architecture example, not a real company deployment. It demonstrates realistic patterns and metrics based on industry best practices.

## Executive Summary

Implemented human-in-the-loop (HITL) remediation system that proposes and executes fix actions with engineer approval. Reduced mean time to resolution (MTTR) from 45 minutes to 12 minutes for common incident types while maintaining 100% human oversight. Combined browser automation (browser-use) for legacy admin panels with MCP servers for modern APIs and StackStorm for workflow orchestration. Achieved 95% approval rate for proposed actions, demonstrating high trust and accuracy.

## Organization Context

### Company Profile

- **Size**: 350 employees, 65 engineers
- **Scale**: 80 services, 15K requests/minute, HIPAA-compliant environment
- **Industry**: Healthcare SaaS (patient management, scheduling)
- **Maturity**: Growth stage (Series C)

### Pre-Implementation State

**Challenges:**
- Manual remediation steps taking 20-40 minutes for well-understood failures
- Legacy admin panels requiring 15+ clicks to perform common operations (no APIs)
- Inconsistent remediation quality (different engineers followed different steps)
- On-call fatigue from repetitive "toil" incidents (cache clears, pod restarts, queue drains)
- Risk of human error during late-night incidents (typos, wrong environment)

**Existing Infrastructure:**
- **Observability**: Elastic Stack (logs), Prometheus/Grafana (metrics)
- **Orchestration**: Kubernetes, AWS
- **Ticketing**: Jira
- **Automation**: Some Ansible playbooks, mostly unused
- **Legacy Systems**: 5 admin panels with no API access

## Goals & Success Criteria

### Primary Goals

1. **Reduce Remediation Toil**: Automate repetitive fix actions with human approval
   - Target: 60% of remediations automated
   - Timeline: 6 months

2. **Decrease MTTR**: Faster execution of approved actions
   - Target: MTTR from 45min to <15min for automated incident types
   - Timeline: 6 months

3. **Reduce Human Error**: Eliminate typos, wrong-environment mistakes
   - Target: <1% error rate in remediation actions
   - Timeline: Ongoing

### Success Metrics

- **MTTR**: Reduce from 45min to <15min (achieved: 12min)
- **Automation Rate**: 60% of incidents (achieved: 68%)
- **Approval Rate**: >80% (achieved: 95%)
- **Error Rate**: <1% (achieved: 0.3%)
- **Engineer Satisfaction**: >70% (achieved: 87%)

## Technical Architecture

### Architecture Diagram

```
┌─────────────────┐
│ Alert (PagerDuty│
│ + Prometheus)   │
└────────┬────────┘
         │
┌────────▼──────────────────┐
│ Investigation Agent       │
│ (Diagnose root cause)     │
└────────┬──────────────────┘
         │
┌────────▼──────────────────┐
│ Remediation Planner       │
│ (Propose fix actions)     │
└────────┬──────────────────┘
         │
┌────────▼──────────────────┐
│ Human Approval            │
│ (Slack interactive msg)   │
└────────┬──────────────────┘
         │
┌────────▼──────────────────┐
│ Execution Layer           │
│                           │
│  ┌───────────────────┐    │
│  │ StackStorm        │    │
│  │ (API actions)     │    │
│  └───────────────────┘    │
│                           │
│  ┌───────────────────┐    │
│  │ browser-use       │    │
│  │ (Legacy UI)       │    │
│  └───────────────────┘    │
│                           │
│  ┌───────────────────┐    │
│  │ kubectl           │    │
│  │ (K8s operations)  │    │
│  └───────────────────┘    │
└────────┬──────────────────┘
         │
┌────────▼──────────────────┐
│ Audit Log + Verification  │
└───────────────────────────┘
```

### Component Stack

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| **Agent** | Claude 3.5 Sonnet | Latest | Diagnosis and remediation planning |
| **Orchestration** | StackStorm | 3.8+ | Workflow automation for API-based actions |
| **Browser Automation** | browser-use | 0.1.x | Legacy admin panel interactions |
| **Tool Access** | Custom MCP Gateway | N/A | Secure API access |
| **Approval UI** | Slack Interactive Messages | N/A | HITL approval interface |
| **Policy** | OPA | 0.60+ | Action approval policies |
| **Audit** | PostgreSQL + Splunk | N/A | Comprehensive action logging |
| **Verification** | Custom | N/A | Post-action validation |

### Key Design Decisions

**Decision 1: HITL instead of full automation**
- **Rationale**: Healthcare compliance requires human oversight; build trust incrementally
- **Trade-offs**: Still requires engineer to approve, but dramatically faster than manual execution
- **Outcome**: 95% approval rate shows high trust; 87% engineer satisfaction

**Decision 2: Browser automation for legacy systems**
- **Rationale**: 5 critical admin panels had no APIs; rewriting them would take 12+ months
- **Trade-offs**: More fragile than API calls, but pragmatic solution
- **Outcome**: Handled 30% of remediation actions; 97% success rate

**Decision 3: Structured action format with pre/post verification**
- **Rationale**: Need to verify action succeeded and didn't cause side effects
- **Trade-offs**: Adds complexity, but critical for safety
- **Outcome**: Caught 8 cases where action "succeeded" but didn't fix the issue

### Security & Governance

**Access Control:**
- Remediation system uses dedicated service account with limited write permissions
- Actions are scoped to specific namespaces/services
- Browser automation runs in isolated containers with session recording

**Approval Workflows:**
- All write actions require explicit engineer approval via Slack
- Approval expires after 5 minutes (prevents stale approvals)
- High-risk actions (production database, patient data) require secondary approval from lead

**Audit & Compliance:**
- All proposed and executed actions logged with: approver, timestamp, before/after state
- Browser automation sessions recorded (video + DOM snapshots)
- Audit logs retained for 7 years (HIPAA requirement)
- Monthly compliance reports with action breakdown

## Implementation Journey

### Phase 1: Proof of Concept (4 weeks)

**Scope**:
- Single action type: Kubernetes pod restart
- Single namespace (non-production)
- 3 volunteer engineers

**Team**: 2 SREs

**Results**:
- 100% success rate on 12 test incidents
- Average time from diagnosis to restart: 2 minutes (vs. 8 minutes manual)
- Decision to proceed with expanded pilot

### Phase 2: Pilot Deployment (3 months)

**Scope**:
- Expanded to 8 action types (pod restart, scale, cache clear, queue drain, etc.)
- Production environment with safeguards
- All SRE team (12 engineers)

**Challenges**:

1. **Challenge: Browser automation too brittle for UI changes**
   - **Solution**: Computer vision-based selectors (Skyvern-style) instead of CSS selectors
   - **Outcome**: Resilience to UI changes increased from 60% to 95%

2. **Challenge: Engineers ignored approval requests during busy incidents**
   - **Solution**: Added "quick approve" with risk score; low-risk actions auto-approved after 60 seconds
   - **Outcome**: Approval latency reduced from 3min to 45sec

3. **Challenge: Verification step sometimes slower than the action itself**
   - **Solution**: Async verification with notification; don't block workflow
   - **Outcome**: End-to-end time reduced by 40%

### Phase 3: Production Rollout (4 months)

**Rollout Strategy**: Incident-type by incident-type, starting with safest

**Adoption Metrics**:
- Month 1: Pod restarts only (safest) - 100% adoption
- Month 2: Added cache clears, scaling - 90% adoption
- Month 4: Added legacy panel actions (queue management) - 68% adoption

## Results & Impact

### Quantitative Results

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **MTTR** | 45 min | 12 min | 73% reduction |
| **Incidents Fully Automated** | 0% | 68% | N/A |
| **Time from Approval to Fix** | 15 min (manual) | 2 min | 87% reduction |
| **Remediation Errors** | 3-5% | 0.3% | 90% reduction |
| **Weekly On-Call Toil Hours** | 8 hrs | 3 hrs | 62% reduction |

### Qualitative Impact

**Team Experience:**
- "I can approve a fix and go back to sleep instead of spending 30min executing it" - On-call Engineer
- "The verification step caught a case where cache clear didn't actually work - saved us hours" - Senior SRE
- "Browser automation for the legacy admin panel is honestly magical" - Platform Engineer

**Organizational Benefits:**
- Reduced on-call burnout (toil hours cut by 62%)
- Standardized remediation procedures (everyone uses same steps)
- Better audit trail for compliance reviews

**Unexpected Wins:**
- Browser automation recordings became training material for new engineers
- Action library became living documentation of "how to fix X"
- Reduced late-night mistakes; system doesn't make typos

## Challenges & Solutions

### Challenge 1: Legacy admin panel sessions timing out

**Problem**: Browser automation sessions lasted 5+ minutes; admin panel timeout was 3 minutes

**Attempted Solutions**:
1. Faster actions - Still hit timeout on complex workflows
2. Session keep-alive pings - Admin panel blocked automation

**Final Solution**:
- Pre-authenticate before diagnosis complete
- Maintain session pool (2 warm sessions per panel)
- Session refresh in background

**Lessons**: Plan for session management in browser automation from day 1

---

### Challenge 2: Risk assessment for approval decisions

**Problem**: Engineers didn't know if proposed action was safe to approve

**Attempted Solutions**:
1. Always show risk as "high" - Engineers ignored it
2. Detailed risk explanation - Too verbose, not read

**Final Solution**:
- Simple risk score (low/medium/high) with 1-sentence reason
- Show blast radius (e.g., "affects 1 pod in staging")
- Historical success rate for this action type

**Lessons**: Risk communication needs to be concise and data-driven

---

### Challenge 3: Partial failures hard to detect

**Problem**: Action "succeeded" but issue persisted (e.g., pod restarted but still crashing)

**Attempted Solutions**:
1. Simple health check - Not comprehensive
2. Wait and see - Too slow

**Final Solution**:
- Multi-stage verification:
  1. Action completed (e.g., pod restarted)
  2. Service healthy (health check passing)
  3. Metrics improved (error rate decreased)
  4. Alert resolved (issue gone)

**Lessons**: Verification needs to check the actual goal, not just action completion

## Lessons Learned

### What Worked Well

1. **HITL approach**: Balances automation with safety; 95% approval rate shows trust
2. **Browser automation**: Pragmatic solution for legacy systems; avoided 12-month rewrite
3. **Structured action format**: Made it easy to add new action types
4. **Slack integration**: Approvals in same tool as incident coordination

### What We'd Do Differently

1. **Build risk assessment framework earlier**: Took 6 weeks to get right; should have been in POC
2. **More conservative rollout**: Tried to add too many action types at once in pilot
3. **Better verification design**: Async verification should have been in initial design

### Surprises & Unexpected Findings

- **Finding 1**: Engineers trusted browser automation more than API calls (could see it working in recordings)
- **Finding 2**: Quick-approve with timeout worked better than expected; eliminated approval latency bottleneck

## Recommendations for Others

### For Similar Organizations

**If you're building HITL remediation:**
- ✅ **Do**: Start with safest actions (read-only, idempotent operations)
- ✅ **Do**: Build comprehensive verification (not just action completion)
- ✅ **Do**: Provide approval UI in same tool as incident management (Slack, Teams)
- ✅ **Do**: Consider browser automation for legacy systems without APIs
- ❌ **Don't**: Skip the risk assessment framework
- ❌ **Don't**: Auto-approve without timeout (engineers need to actively approve)
- ❌ **Don't**: Forget about session management for browser automation

### Prerequisites

Before attempting this implementation, ensure you have:

- [x] Clear inventory of common remediation actions
- [x] Approval workflow tool (Slack, Teams, etc.)
- [x] Audit logging infrastructure
- [x] Verification mechanisms (health checks, metrics)
- [x] Security team buy-in for automated actions

### Estimated Resources

**Time**: 4-6 months with 2 FTE engineers

**Budget**:
- Infrastructure: $400/month (browser automation VMs, databases)
- LLM API: $500-1000/month
- StackStorm: Self-hosted (included in infra costs)
- Development: ~$200K in engineering time

**Team**: 2 senior SREs (one with automation experience)

## Future Plans

### Short-Term (Next 3-6 months)

- Add database query actions (read-only introspection)
- Improve risk scoring with ML model
- Multi-step remediations (not just single actions)

### Long-Term (Next 12 months)

- Conditional auto-approval (for actions with 100% historical success)
- Predictive remediation (suggest fixes before alert fires)
- Integration with change management system

## Appendix

### Sample Action Definition

```yaml
# Action: Restart Pod
action_id: k8s_pod_restart
category: kubernetes
risk_level: low
approval_required: true

parameters:
  - name: namespace
    type: string
    required: true
  - name: pod_name
    type: string
    required: true

pre_conditions:
  - pod_exists
  - namespace_not_production_critical

execution:
  tool: kubectl
  command: "delete pod {{ pod_name }} -n {{ namespace }}"

verification:
  - check: pod_recreated
    timeout: 60s
  - check: pod_healthy
    timeout: 120s
  - check: error_rate_decreased
    timeout: 300s

audit:
  log_level: info
  record_before_state: true
  record_after_state: true
```

### Sample Slack Approval Message

```
🤖 Remediation Proposed

**Incident**: High error rate in user-service
**Root Cause**: Memory leak in pod user-service-7d9f8-abc123
**Proposed Action**: Restart pod

**Details:**
  Namespace: production
  Pod: user-service-7d9f8-abc123
  Risk: 🟢 Low
  Blast Radius: 1 pod (rolling restart, no downtime)
  Success Rate: 98% (last 50 executions)

[Approve] [Reject] [Details]

This approval expires in 5 minutes
```

### References

- [browser-use Framework](https://github.com/browser-use/browser-use)
- [StackStorm Documentation](https://docs.stackstorm.com/)
- [HITL Design Patterns](https://arxiv.org/abs/2104.05404)

---

## Contact

**Author**: Reference Architecture Example

**Organization**: N/A - Educational Template

**Questions?**: Please open a discussion in the [awesome-autonomous-ops repository](https://github.com/nik-kale/awesome-autonomous-ops/discussions)

---

**Last updated**: December 2024

**Version**: 1.0

