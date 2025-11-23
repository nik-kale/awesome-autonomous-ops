# awesome-autonomous-ops

> A curated map of **AI-powered autonomous operations, SRE, and support agents** — Graph RAG for logs, agentic remediation, MCP connectors, and browser-based ops assistants.

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

## Introduction

**Autonomous operations** is the convergence of AI, observability, and reliability engineering. It's not just about chatbots answering questions — it's about AI agents that can **diagnose incidents**, **execute remediation runbooks**, **navigate ops consoles**, and **coordinate across toolchains** with appropriate safety guardrails.

This list curates the essential building blocks for AI-powered SRE, DevOps, and SecOps workflows: graph-based root cause analysis over logs and metrics, agentic systems that troubleshoot and heal production, Model Context Protocol (MCP) servers that safely expose operational tools to AI, and browser automation frameworks that let agents interact with dashboards and consoles. Whether you're building intelligent on-call assistants, autonomous incident responders, or AI-augmented support fabrics, these projects represent the state of the art.

The goal is to provide a **reference architecture** for practitioners: clear, composable, and production-minded tools that respect the complexity and criticality of real-world operations.

## Contents

- [Getting Started](#getting-started)
- [Projects by the Curator](#projects-by-the-curator)
- [Graph RAG & Root Cause Analysis for Logs and Incidents](#graph-rag--root-cause-analysis-for-logs-and-incidents)
- [Agentic Remediation & Runbooks](#agentic-remediation--runbooks)
- [MCP Servers & Gateways for Autonomous Ops](#mcp-servers--gateways-for-autonomous-ops)
- [Browser & Desktop Ops Agents](#browser--desktop-ops-agents)
- [Compliance, Governance, and Safety for AI Ops](#compliance-governance-and-safety-for-ai-ops)
- [Datasets, Simulators, and Labs](#datasets-simulators-and-labs)
- [How to Use This List](#how-to-use-this-list)
- [Resources](#resources)
- [Contributing](#contributing)
- [License](#license)

## Getting Started

New to autonomous operations? Start here:

- **[Getting Started Guide](GETTING-STARTED.md)** - Build your first autonomous ops system in 30 minutes
- **[Tool Comparisons](COMPARISONS.md)** - Side-by-side comparison of tools to help you choose
- **[Reference Architectures](ARCHITECTURES.md)** - Proven patterns for read-only, HITL, and fully autonomous systems
- **[Glossary](GLOSSARY.md)** - Terminology and concepts explained
- **[Case Studies](case-studies/)** - Real-world implementations and lessons learned
- **[Roadmap](ROADMAP.md)** - Future vision and planned features

## Projects by the Curator

I am an architect of AI-powered support and autonomous operations systems, including the Cisco AI Support Fabric and the ADAPT (Adaptive Diagnostic and Problem-solving Tools) framework. The following projects represent reference implementations and core infrastructure for building production-grade autonomous ops environments:

- **[AutoRCA-Core (ADAPT-RCA)](https://github.com/nik-kale/AutoRCA-Core)** *(coming soon)* – Graph RAG and multi-signal root cause analysis engine for autonomous reliability. Combines time-series correlation, dependency graphs, and LLM reasoning to identify incident causes across logs, metrics, traces, and configuration changes.

- **[Secure-MCP-Gateway](https://github.com/nik-kale/Secure-MCP-Gateway)** *(coming soon)* – Security-first Model Context Protocol gateway for operational tools (Jira, Splunk, Kubernetes, GitHub, PagerDuty). Provides policy-based access control, human-in-the-loop approvals for write actions, and comprehensive audit trails for AI agent interactions with production systems.

- **[Ops-Agent-Desktop](https://github.com/nik-kale/Ops-Agent-Desktop)** *(coming soon)* – Visual mission control UI for autonomous SRE and support agents. Real-time visualization of agent investigations and remediations, with browser automation to show live interactions with ops consoles and dashboards.

- **[ADAPT-Agents](https://github.com/nik-kale/ADAPT-Agents)** *(coming soon)* – Modular library of diagnostic and troubleshooting agents for common operational scenarios. Designed to work with AutoRCA-Core for root cause analysis and Secure-MCP-Gateway for safe tool access.

- **[Secure-AI-Support-Fabric](https://github.com/nik-kale/Secure-AI-Support-Fabric)** *(coming soon)* – Hands-on autonomous operations lab and reference implementation. Demonstrates end-to-end AI-powered incident response, from detection through diagnosis to remediation, with proper security boundaries and human oversight.

## Graph RAG & Root Cause Analysis for Logs and Incidents

Tools that perform retrieval-augmented generation, graph-based reasoning, and correlation analysis over operational telemetry to identify incident root causes.

- **[AutoRCA-Core (ADAPT-RCA)](https://github.com/nik-kale/AutoRCA-Core)** *(coming soon)* – Agentic RCA engine with graph-based reasoning over logs, metrics, traces, and configuration changes. Reference implementation for autonomous reliability workflows.

- **[Sage](https://github.com/apple/ml-sage)** – Apple's system for grounding LLM reasoning in structured incident data. Uses semantic search and entity graphs to improve diagnostic accuracy.

- **[LangGraph](https://github.com/langchain-ai/langgraph)** – Framework for building stateful, graph-based AI workflows. Useful for orchestrating multi-step diagnostic and remediation processes with cyclical reasoning.

- **[txtai](https://github.com/neuml/txtai)** – Embeddings database for semantic search over logs and documentation. Enables RAG workflows for incident troubleshooting and knowledge retrieval.

- **[Haystack](https://github.com/deepset-ai/haystack)** – End-to-end framework for building RAG pipelines. Can be adapted for log analysis and incident documentation search.

## Agentic Remediation & Runbooks

Systems where AI agents autonomously execute or orchestrate remediation actions, runbooks, and operational procedures.

- **[Kubiya](https://github.com/kubiyabot/community-tools)** – Conversational AI agent for DevOps workflows. Integrates with Kubernetes, Terraform, and CI/CD pipelines for automated operations.

- **[Rundeck](https://github.com/rundeck/rundeck)** – Runbook automation and operational orchestration platform. Can be integrated with AI agents for intelligent remediation workflows.

- **[StackStorm](https://github.com/StackStorm/st2)** – Event-driven automation platform for auto-remediation. Connects sensors, triggers, and actions across infrastructure and tools.

- **[Ansible Rulebooks](https://github.com/ansible/ansible-rulebook)** – Event-driven automation using Ansible. Enables reactive remediation based on observability signals and alerts.

- **[Robusta](https://github.com/robusta-dev/robusta)** – Kubernetes troubleshooting and automation platform. Provides diagnostic playbooks and auto-remediation capabilities.

## MCP Servers & Gateways for Autonomous Ops

Model Context Protocol servers and gateways that expose operational tools, ticketing systems, observability platforms, and infrastructure APIs to AI agents with appropriate security controls.

- **[Secure-MCP-Gateway](https://github.com/nik-kale/Secure-MCP-Gateway)** *(coming soon)* – Security-first MCP gateway specifically designed for autonomous operations. Features policy-based access control, human-in-the-loop approval workflows for write operations, comprehensive audit logging, and pre-built connectors for Jira, Splunk, Kubernetes, GitHub, and PagerDuty. Reference implementation for safe AI agent access to production systems.

- **[MCP Servers for Kubernetes](https://github.com/kubernetes/kubernetes)** – MCP-compatible interfaces for Kubernetes resources. Enables AI agents to query cluster state and (with proper guardrails) execute kubectl commands.

- **[PulseMCP](https://github.com/pulsemcp/pulsemcp)** – Community directory of MCP servers, including ops-focused implementations for observability and infrastructure tools.

- **[awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers)** – Curated list of MCP servers across domains. Filter for observability, infrastructure, and DevOps categories for ops-relevant integrations.

- **[MCP GitHub Server](https://github.com/modelcontextprotocol/servers/tree/main/src/github)** – Official MCP server for GitHub API access. Useful for automated incident ticket creation and PR-based remediation workflows.

- **[MCP Prometheus Server](https://github.com/modelcontextprotocol/servers/tree/main/src/prometheus)** – Official MCP server for Prometheus metrics. Enables AI agents to query time-series data during diagnostic investigations.

## Browser & Desktop Ops Agents

Browser automation frameworks and desktop agents that let AI navigate operational consoles, dashboards, and web-based tools that lack programmatic APIs.

- **[Ops-Agent-Desktop](https://github.com/nik-kale/Ops-Agent-Desktop)** *(coming soon)* – Visual mission control for autonomous SRE agents. Combines browser automation with real-time visualization of investigation and remediation workflows. Reference implementation for observability into agent behavior.

- **[browser-use](https://github.com/browser-use/browser-use)** – Framework for building AI agents that control web browsers. Useful for navigating dashboards and consoles that lack APIs.

- **[Skyvern](https://github.com/Skyvern-AI/skyvern)** – Browser automation framework using computer vision and LLMs. Enables agents to interact with complex web UIs without brittle selectors.

- **[LaVague](https://github.com/lavague-ai/LaVague)** – AI-powered web agent framework for automating browser interactions. Can be adapted for ops console navigation.

- **[Playwright](https://github.com/microsoft/playwright)** – Browser automation library with robust APIs. Foundation for building custom ops agents that interact with web dashboards.

## Compliance, Governance, and Safety for AI Ops

Tools and frameworks for establishing guardrails, approval workflows, policy enforcement, and audit trails around AI agents operating in production environments.

- **[Responsible-AI-Compliance-Blueprint](https://github.com/nik-kale/Responsible-AI-Compliance-Blueprint)** *(coming soon)* – Comprehensive framework for governance, risk management, and compliance in autonomous operations systems.

- **[Open Policy Agent (OPA)](https://github.com/open-policy-agent/opa)** – Policy-based control framework. Can be used to define and enforce policies for AI agent actions in production.

- **[Falco](https://github.com/falcosecurity/falco)** – Runtime security monitoring for cloud-native environments. Useful for detecting anomalous agent behavior and policy violations.

- **[NeMo Guardrails](https://github.com/NVIDIA/NeMo-Guardrails)** – Framework for adding programmable guardrails to LLM applications. Applicable to constraining agent behavior in ops workflows.

- **[LangKit](https://github.com/whylabs/langkit)** – LLM observability and monitoring toolkit. Provides safety metrics and guardrail monitoring for AI agents.

## Datasets, Simulators, and Labs

Datasets, simulation environments, and hands-on labs for developing, testing, and benchmarking autonomous operations systems.

- **[ADAPT-Data](https://github.com/nik-kale/ADAPT-Data)** *(coming soon)* – Synthetic and anonymized operational datasets for training and evaluating RCA and diagnostic agents.

- **[Secure-AI-Support-Fabric](https://github.com/nik-kale/Secure-AI-Support-Fabric)** *(coming soon)* – Complete lab environment for autonomous ops. Includes instrumented applications, observability stack, and sample incident scenarios.

- **[Chaos Mesh](https://github.com/chaos-mesh/chaos-mesh)** – Chaos engineering platform for Kubernetes. Useful for generating realistic failure scenarios to test autonomous remediation.

- **[Gremlin](https://github.com/gremlin/gremlin-python)** – Chaos engineering tools and failure injection. Enables controlled testing of agent response to production incidents.

- **[OpenTelemetry Demo](https://github.com/open-telemetry/opentelemetry-demo)** – Microservices demo with full observability instrumentation. Provides realistic telemetry data for testing diagnostic agents.

- **[LogHub](https://github.com/logpai/loghub)** – Large collection of real-world system logs for research and development. Useful for training log analysis and anomaly detection models.

## How to Use This List

This list is organized as a **composable reference architecture** for AI-powered autonomous operations:

**Start with observability and RCA**: Use Graph RAG and root cause analysis tools to give your agents the ability to understand what's happening in your systems. Tools like AutoRCA-Core, txtai, and LangGraph form the diagnostic foundation.

**Add safe tool access**: Deploy MCP servers and gateways to expose operational tools (Kubernetes, Jira, Splunk, GitHub) to your agents with proper security controls. Secure-MCP-Gateway provides a reference implementation with policy enforcement and human-in-the-loop approvals.

**Orchestrate remediation**: Integrate agentic remediation frameworks (StackStorm, Rundeck, Robusta) to let agents execute runbooks and recovery procedures based on their diagnostic findings.

**Handle console-only tools**: For systems without APIs, use browser automation frameworks (browser-use, Skyvern, Playwright) to let agents navigate web dashboards and legacy interfaces.

**Enforce governance**: Layer in compliance and safety tools (OPA, NeMo Guardrails, Falco) to constrain agent behavior, enforce policies, and maintain audit trails.

**Test and iterate**: Use simulation environments and datasets (Chaos Mesh, ADAPT-Data, OpenTelemetry Demo) to develop and validate your autonomous ops workflows before production deployment.

The goal is not to build a single monolithic "AI ops platform," but rather to compose small, well-defined, interoperable components into a system that matches your operational context and risk tolerance.

## Resources

### Documentation

- **[Getting Started Guide](GETTING-STARTED.md)** - Practical guide to building your first autonomous ops system
- **[Tool Comparisons](COMPARISONS.md)** - Detailed comparison matrices for all tool categories
- **[Reference Architectures](ARCHITECTURES.md)** - Three production-ready architectural patterns
- **[Glossary](GLOSSARY.md)** - Comprehensive terminology reference
- **[Security Policy](SECURITY.md)** - Security practices and responsible disclosure

### Community

- **[Discussions](https://github.com/nik-kale/awesome-autonomous-ops/discussions)** - Ask questions, share ideas, connect with practitioners
- **[Case Studies](case-studies/)** - Real-world implementations and lessons learned
- **[Issue Templates](https://github.com/nik-kale/awesome-autonomous-ops/issues/new/choose)** - Submit projects, report issues, suggest improvements

### Planning & Vision

- **[Roadmap](ROADMAP.md)** - Strategic evolution plan (Version 2.0, 3.0, 4.0)
- **[Contributing Guidelines](CONTRIBUTING.md)** - How to contribute to this resource
- **[Code of Conduct](CODE_OF_CONDUCT.md)** - Community standards and expectations

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on proposing new entries, reporting issues, or suggesting improvements.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

Curated by [Nik Kale](https://github.com/nik-kale) · Principal Engineer & Architect · AI-Powered Autonomous Operations and Reliability
