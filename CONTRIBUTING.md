# Contributing to awesome-autonomous-ops

Thank you for your interest in contributing to `awesome-autonomous-ops`! This guide explains how to propose new entries, suggest improvements, and maintain the quality and focus of this curated list.

## What Belongs in This List

This list focuses specifically on **AI-powered autonomous operations, SRE, DevOps, and support systems**. Projects should fall into one or more of these categories:

- **Graph RAG and Root Cause Analysis**: Tools that use retrieval-augmented generation, graph reasoning, or correlation analysis over logs, metrics, traces, and operational data to diagnose incidents.

- **Agentic Remediation and Runbooks**: Systems where AI agents autonomously execute or orchestrate remediation actions, recovery procedures, or operational runbooks.

- **MCP Servers and Gateways for Ops**: Model Context Protocol implementations that expose operational tools (observability platforms, ticketing systems, infrastructure APIs) to AI agents with appropriate security controls.

- **Browser and Desktop Ops Agents**: Browser automation frameworks and desktop agents that enable AI to navigate operational consoles, dashboards, and web-based tools.

- **Compliance, Governance, and Safety**: Tools for establishing guardrails, policy enforcement, approval workflows, and audit trails for AI agents operating in production environments.

- **Datasets, Simulators, and Labs**: Resources for developing, testing, and benchmarking autonomous operations systems, including synthetic data, failure injection platforms, and hands-on lab environments.

## Submission Requirements

Before proposing a new entry, please ensure it meets these criteria:

1. **Open Source**: The project must be open source with a recognized license (MIT, Apache 2.0, GPL, etc.). Commercial-only or closed-source tools are not eligible.

2. **Relevance**: The project must be directly relevant to **autonomous operations, SRE, DevOps, or support workflows**. General-purpose AI tools, chatbots without ops integration, or generic automation frameworks typically don't qualify unless they have clear application to operational reliability.

3. **Maintenance**: The project should show signs of active maintenance or be a well-established, stable tool. Check for:
   - Recent commits (within the last 12 months for active projects)
   - Responsive issue/PR management
   - Clear documentation
   - Production readiness or significant community adoption

4. **Quality**: The project should demonstrate technical quality:
   - Clear documentation (README with architecture overview, quickstart, etc.)
   - Well-structured codebase
   - Tests and/or examples
   - Professional presentation

5. **No Duplicates**: Check that the project isn't already listed. If a similar tool exists in the list, your submission should clearly explain the unique value or differentiation.

## How to Submit a New Entry

### 1. Choose the Right Category

Identify which section(s) of the README your project belongs in:

- Graph RAG & Root Cause Analysis for Logs and Incidents
- Agentic Remediation & Runbooks
- MCP Servers & Gateways for Autonomous Ops
- Browser & Desktop Ops Agents
- Compliance, Governance, and Safety for AI Ops
- Datasets, Simulators, and Labs

If your project spans multiple categories, choose the **primary** category based on its core value proposition.

### 2. Format Your Entry

Use this format:

```markdown
- **[Project Name](https://github.com/owner/repo)** – One clear, concise sentence (under 150 characters) describing what the project does and its relevance to autonomous ops. Mention whether it's focused on RAG, MCP, agents, observability, etc.
```

**Examples**:

```markdown
- **[Sage](https://github.com/apple/ml-sage)** – Apple's system for grounding LLM reasoning in structured incident data. Uses semantic search and entity graphs to improve diagnostic accuracy.

- **[Robusta](https://github.com/robusta-dev/robusta)** – Kubernetes troubleshooting and automation platform. Provides diagnostic playbooks and auto-remediation capabilities.
```

### 3. Submit a Pull Request

1. **Fork** this repository.
2. **Create a branch** for your addition: `git checkout -b add-project-name`
3. **Add your entry** to the appropriate section in `README.md`, maintaining alphabetical order within each section (except for featured/curator projects at the top).
4. **Commit** your change: `git commit -m "Add [Project Name] to [Category]"`
5. **Push** to your fork: `git push origin add-project-name`
6. **Open a Pull Request** against the `main` branch with:
   - A clear title: "Add [Project Name]"
   - A brief description explaining why the project is relevant to autonomous ops
   - Links to documentation, demos, or case studies if available

### 4. Review Process

Pull requests will be reviewed based on:

- **Relevance**: Does this project clearly advance autonomous operations, SRE, or AI-powered support workflows?
- **Quality**: Is the project well-documented, maintained, and production-ready or on a clear path to production readiness?
- **Presentation**: Is the description clear, concise, and accurately positioned within the autonomous ops ecosystem?

The maintainer may request changes to the description, category placement, or ask for additional context before merging.

## Suggesting Improvements

Beyond adding new projects, you can contribute by:

- **Fixing broken links**: If a project has moved or been archived, please submit a PR to update or remove it.
- **Improving descriptions**: If an existing entry's description is unclear or outdated, suggest a better one.
- **Reorganizing sections**: If you think the taxonomy could be improved, open an issue to discuss structural changes.
- **Adding context**: If you've used a listed tool in production autonomous ops workflows, consider adding a brief note or link to a case study.

## What Will Not Be Accepted

To maintain focus and quality, the following will generally not be accepted:

- **Generic AI/LLM tools** without clear operational focus (e.g., general-purpose chatbots, content generation tools).
- **Closed-source or commercial-only products** without an open-source core.
- **Abandoned projects** with no maintenance activity in 2+ years and no clear indication of stability/completion.
- **Self-promotion without substance**: Projects must stand on their own merit. If you're submitting your own project, ensure it meets all quality and relevance criteria.
- **Duplicates**: If a project is functionally identical to an existing entry, it won't be added unless it offers clear differentiation.

## Code of Conduct

This project adheres to a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold a respectful, inclusive, and professional environment.

## Questions?

If you're unsure whether a project fits, or you have questions about the contribution process, please open an issue to discuss before submitting a PR. We're happy to provide guidance.

---

Thank you for helping build the definitive resource for AI-powered autonomous operations!
