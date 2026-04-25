# Case Study: Slack-Based Investigation Assistant

> **Anonymization Level**: Reference Architecture Example
>
> **Industry**: Financial Services
>
> **Deployment Date**: Q1 2025
>
> **Last Updated**: December 2024

> ⚠️ **Note**: This is a reference architecture example, not a real company deployment. It demonstrates realistic patterns and metrics based on industry best practices.

## Executive Summary

Deployed conversational AI investigation assistant integrated with Slack, providing on-call engineers with instant access to logs, metrics, and system state through natural language queries. Reduced initial investigation time by 55% and improved incident handoff quality by providing automatically generated context summaries. Implemented strict read-only access via MCP servers with comprehensive audit logging. Achieved 88% engineer adoption within 3 months of rollout.

## Organization Context

### Company Profile

- **Size**: 800 employees, 120 engineers
- **Scale**: 300 microservices, 2M transactions/day, highly regulated environment
- **Industry**: Payment processing and financial services
- **Maturity**: Enterprise (10+ years in business)

### Pre-Implementation State

**Challenges:**
- On-call engineers switching between 8+ tools during investigations (Splunk, Grafana, Jira, internal dashboards)
- Context loss during incident handoffs between shifts (24/7 operations)
- Junior engineers struggling to formulate correct Splunk queries
- Knowledge silos - only senior engineers knew where to look for certain types of issues
- High cognitive load navigating complex permission structures across tools

**Existing Infrastructure:**
- **Observability**: Splunk (logs), Datadog (metrics/APM), PagerDuty (alerts)
- **Orchestration**: Kubernetes, Terraform
- **Ticketing**: ServiceNow
- **Communication**: Slack (primary), Zoom
- **Existing Bots**: Basic notification bots, no investigation capabilities

## Goals & Success Criteria

### Primary Goals

1. **Single Interface for Investigation**: Replace tool-switching with conversational interface
   - Target: 80% of investigation queries answerable via Slack
   - Timeline: 6 months

2. **Democratize Troubleshooting**: Enable junior engineers to investigate effectively
   - Target: Junior engineers handling 50% more incidents without escalation
   - Timeline: 12 months

3. **Improve Handoff Quality**: Auto-generate incident summaries
   - Target: 90% of handoffs include complete context
   - Timeline: Ongoing

### Success Metrics

- **Tool Context Switches**: Reduce from 8 to <3 per incident (achieved: 2.5)
- **Time to First Clue**: <2 minutes (achieved: 1.5 min)
- **Engineer Adoption**: >70% (achieved: 88%)
- **Handoff Completeness**: >80% (achieved: 92%)

## Technical Architecture

### Architecture Diagram

```
┌─────────────────────┐
│ Slack (Engineer)    │
└──────────┬──────────┘
           │
┌──────────▼──────────────────┐
│ Investigation Bot           │
│ (Claude 3.5 + LangChain)    │
│                             │
│  ┌──────────────────────┐   │
│  │ Query Understanding  │   │
│  │ Tool Selection       │   │
│  │ Response Formatting  │   │
│  └──────────────────────┘   │
└──────────┬──────────────────┘
           │
┌──────────▼──────────────────┐
│ MCP Gateway                 │
│ (Secure Tool Access)        │
│                             │
│  ┌──────────────────┐       │
│  │ Policy Engine    │       │
│  │ (OPA)            │       │
│  └──────────────────┘       │
│                             │
│  ┌──────────────────┐       │
│  │ Audit Logger     │       │
│  └──────────────────┘       │
└──────────┬──────────────────┘
           │
     ┌─────▼─────┐
     │           │
┌────▼────┐ ┌───▼────┐ ┌────▼────┐
│ Splunk  │ │ Datadog│ │ K8s API │
│ MCP     │ │ MCP    │ │ MCP     │
└─────────┘ └────────┘ └─────────┘
```

### Component Stack

| Layer | Technology | Version | Purpose |
|-------|------------|---------|---------|
| **Agent** | Claude 3.5 Sonnet | Latest | Query understanding and response generation |
| **Framework** | LangChain | 0.1.x | Agent orchestration |
| **Gateway** | Custom MCP Gateway | N/A | Secure tool access and policy enforcement |
| **Policy** | Open Policy Agent | 0.60+ | RBAC and query restrictions |
| **Audit** | Custom + Splunk | N/A | Comprehensive action logging |
| **MCP Servers** | Custom (Splunk, Datadog, K8s) | N/A | Read-only API adapters |
| **Interface** | Slack Bot API | N/A | User interaction |

### Key Design Decisions

**Decision 1: Conversational interface over command syntax**
- **Rationale**: Natural language lowers barrier for junior engineers and reduces cognitive load
- **Trade-offs**: Requires more sophisticated NLU vs. simple command parsing
- **Outcome**: 88% adoption vs. 30% for previous command-based tools

**Decision 2: Read-only access with no write operations**
- **Rationale**: Financial services compliance requires conservative approach; investigation only
- **Trade-offs**: Cannot automate remediations, but acceptable for Phase 1
- **Outcome**: Passed security review in 2 weeks vs. 6+ months for write access

**Decision 3: User-scoped permissions via MCP gateway**
- **Rationale**: Bot should not have more access than requesting engineer
- **Trade-offs**: More complex implementation than single service account
- **Outcome**: Critical for compliance; bot inherits user's existing RBAC

### Security & Governance

**Access Control:**
- Bot uses engineer's identity for all backend calls (OAuth token passthrough)
- OPA policies enforce service-level restrictions (e.g., production vs. staging)
- No elevated permissions; bot cannot see more than engineer can via UI

**Approval Workflows:**
- N/A (read-only operations only)
- Sensitive queries (customer data) require explicit `/confirm` command

**Audit & Compliance:**
- All queries logged with: engineer ID, timestamp, query text, tools accessed, data returned
- Audit logs retained for 7 years (regulatory requirement)
- Monthly compliance reports auto-generated

## Implementation Journey

### Phase 1: Proof of Concept (3 weeks)

**Scope**:
- Single Slack channel (#sre-poc)
- Splunk queries only
- 5 volunteer engineers

**Team**: 1 senior SRE, 1 platform engineer

**Results**:
- 90% positive feedback from volunteers
- Identified need for better query disambiguation ("logs for what service?")
- Decision to proceed with pilot

### Phase 2: Pilot Deployment (2 months)

**Scope**:
- All SRE team members (20 engineers)
- Added Datadog metrics and Kubernetes access
- Integrated with existing incident channels

**Challenges**:

1. **Challenge: Permission inheritance complexity**
   - **Solution**: Built MCP gateway to translate Slack user to backend identities
   - **Outcome**: Seamless permission model matching existing RBAC

2. **Challenge: Response formatting for large log results**
   - **Solution**: Summarization layer + "show more" pagination
   - **Outcome**: Reduced Slack message noise by 80%

3. **Challenge: Query ambiguity ("show me errors")**
   - **Solution**: Agent asks clarifying questions (service? time range?)
   - **Outcome**: 95% queries successfully executed after clarification

### Phase 3: Production Rollout (3 months)

**Rollout Strategy**: Team-by-team (SRE → Platform → Backend → Frontend)

**Adoption Metrics**:
- Month 1: SRE team (20 engineers) - 100% adoption
- Month 2: Platform team (15 engineers) - 85% adoption
- Month 3: All engineering (120 engineers) - 88% adoption

## Results & Impact

### Quantitative Results

| Metric | Before | After | Improvement |
|--------|--------|-------|-------------|
| **Time to First Clue** | 5 min | 1.5 min | 70% reduction |
| **Tool Context Switches** | 8 | 2.5 | 69% reduction |
| **Junior Engineer Escalations** | 45% | 25% | 44% reduction |
| **Handoffs with Context** | 40% | 92% | 130% increase |
| **Slack Messages in Incident Channels** | 120/incident | 65/incident | 46% reduction (less noise) |

### Qualitative Impact

**Team Experience:**
- "I can finally participate in incidents for services I don't own" - Junior Engineer
- "Handoffs are so much easier - just `/summarize` and I have full context" - On-call Lead
- "Reduced my stress level significantly; I don't feel lost anymore" - Mid-level Engineer

**Organizational Benefits:**
- Flattened learning curve for incident response skills
- Reduced dependency on "hero" senior engineers
- Improved documentation discovery (bot surfaces relevant runbooks)

**Unexpected Wins:**
- Engineers use bot during development to debug (not just incidents)
- Bot queries revealed missing Datadog dashboards - built 12 new dashboards based on common queries
- Generated training material from real investigation conversations

## Challenges & Solutions

### Challenge 1: Rate limiting and cost control

**Problem**: Early beta had no rate limits; one engineer's exploratory session cost $40 in API calls

**Attempted Solutions**:
1. Per-user rate limit (10 queries/hour) - Too restrictive during active incidents
2. Cost warnings after $5 spent - Ignored during incidents

**Final Solution**: Tiered rate limiting
- Normal mode: 20 queries/hour
- Incident mode (in incident channel): unlimited
- Cost dashboard visible to team lead

**Lessons**: Rate limits need incident-aware context

---

### Challenge 2: Hallucination of log queries

**Problem**: Bot occasionally generated invalid Splunk queries that looked correct

**Attempted Solutions**:
1. Few-shot examples in prompt - Helped but not sufficient
2. Query validation API - Too slow

**Final Solution**: 
- MCP server validates query syntax before execution
- If invalid, error returned to agent with syntax hint
- Agent retries with correction (max 2 attempts)

**Lessons**: Always validate generated queries before execution

---

### Challenge 3: PII exposure in logs

**Problem**: Customer data occasionally appeared in error logs; bot could return it

**Attempted Solutions**:
1. PII redaction at display time - Inconsistent
2. Block all queries mentioning customer IDs - Too restrictive

**Final Solution**:
- Splunk MCP server automatically redacts PII patterns (emails, SSNs, card numbers) before returning
- Audit log captures full response for compliance review
- `/show-redacted` command available with justification prompt

**Lessons**: PII handling must be defense-in-depth (multiple layers)

## Lessons Learned

### What Worked Well

1. **Natural language interface**: Dramatically lowered barrier to entry for junior engineers
2. **User-scoped permissions**: Critical for compliance and trust
3. **Incident channel integration**: Bot automatically available in right context
4. **Summary generation**: `/summarize` command became most-loved feature

### What We'd Do Differently

1. **Build cost controls from day 1**: Learned this the hard way
2. **More structured query templates**: Balance between NL flexibility and reliability
3. **Better onboarding flow**: Some engineers didn't know what to ask; need example gallery

### Surprises & Unexpected Findings

- **Finding 1**: Engineers started using bot for non-incident queries (debugging, exploration) - 40% of usage
- **Finding 2**: `/explain` command (explain what this error means) more popular than expected

## Recommendations for Others

### For Similar Organizations

**If you're building investigation assistants:**
- ✅ **Do**: Implement user-scoped permissions (bot as user, not privileged service account)
- ✅ **Do**: Provide conversation history export for incident reports
- ✅ **Do**: Build rate limiting and cost controls from start
- ❌ **Don't**: Skip PII redaction layer
- ❌ **Don't**: Make bot smarter than your senior engineers (they'll distrust it)

### Prerequisites

Before attempting this implementation, ensure you have:

- [x] Slack workspace with bot development enabled
- [x] Centralized logging and metrics platforms with APIs
- [x] Clear RBAC model for existing tools
- [x] Executive sponsorship for tool expenditure (~$1K/month)
- [x] Security team buy-in for audit logging approach

### Estimated Resources

**Time**: 3-4 months with 2 FTE engineers

**Budget**:
- Infrastructure: $200/month (bot hosting, databases)
- LLM API: $800-1500/month depending on usage
- Development: ~$150K in engineering time

**Team**: 1 senior SRE, 1 platform engineer (Slack API experience)

## Future Plans

### Short-Term (Next 3-6 months)

- Add ServiceNow integration for ticket creation with investigation summary
- Multi-step investigation workflows (not just single queries)
- Better visualization of metrics (inline charts in Slack)

### Long-Term (Next 12 months)

- Proactive suggestions (bot suggests what to check next)
- Learning from past incidents (pattern recognition)
- Limited remediation actions (pod restarts, cache clears)

## Appendix

### Sample Conversations

**Example 1: Log Query**
```
Engineer: show me errors in payment-service in the last hour
Bot: 🔍 Searching Splunk logs for payment-service (last 60 minutes)...
     Found 23 errors. Top 3:
     
     [12:45:32] ERROR: Database connection timeout after 30s
     [12:46:01] ERROR: Database connection timeout after 30s
     [12:47:18] ERROR: Database connection timeout after 30s
     
     Pattern: 23 identical "Database connection timeout" errors
     
     💡 Suggestion: Check database-service health
     📊 Show metrics | 📋 Full logs | ❓ Explain error
```

**Example 2: Incident Summary**
```
Engineer: /summarize
Bot: 📝 Incident Summary (last 45 minutes):
     
     **Timeline:**
     12:45 - Payment errors started (23 occurrences)
     12:50 - Engineer Alice investigated logs
     12:52 - Found database connection timeouts
     12:55 - Checked database-service metrics (high CPU)
     13:00 - Scaled database replicas 3→5
     13:05 - Errors stopped
     
     **Root Cause:** Database connection pool exhaustion
     **Resolution:** Scaled replicas
     **Action Items:** Review connection pool sizing
     
     📋 Copy to ServiceNow | 📊 Full details
```

### Sample OPA Policy

```rego
# Only allow access to services the engineer owns or has oncall responsibility for
package mcp.splunk

default allow = false

allow {
    input.user_teams[_] == data.services[input.service].owner_team
}

allow {
    input.user_id == data.oncall_schedule[input.service].current_oncall
}

# Admins can access all services
allow {
    input.user_roles[_] == "admin"
}
```

### References

- [Slack Bot API Documentation](https://api.slack.com/bot-users)
- [Model Context Protocol Specification](https://modelcontextprotocol.io/)
- [Open Policy Agent Documentation](https://www.openpolicyagent.org/docs/)

---

## Contact

**Author**: Reference Architecture Example

**Organization**: N/A - Educational Template

**Questions?**: Please open an issue in the [awesome-autonomous-ops repository](https://github.com/nik-kale/awesome-autonomous-ops/issues)

---

**Last updated**: December 2024

**Version**: 1.0

