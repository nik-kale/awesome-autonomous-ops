# Changelog

All notable changes to awesome-autonomous-ops will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.1.0] - 2026-04-25

### Added

- **[KubeStellar Console](https://github.com/kubestellar/console)** — AI-powered multi-cluster Kubernetes dashboard added to the Agentic Remediation & Runbooks section (CNCF Sandbox, Apache 2.0). Contributed by @clubanderson in PR #17.

### Fixed

- **Project Health Tracking workflow** — Daily scheduled workflow was failing because `.gitignore` blocked `data/*.json` from being committed. Changed to `git add -f` so generated metrics, badges, and RSS feed data are published correctly.

### Changed

- **CI hardening** — Added least-privilege `permissions:` blocks to all workflow files. Pinned `aquasecurity/trivy-action` from `@master` to `@v0.36.0`. Gated Slack notification steps on `SLACK_WEBHOOK_URL` secret presence to eliminate noise on forks and unconfigured repos. Switched CI validation to use pinned `requirements.txt` instead of ad-hoc `pip install`.
- **Dependabot bumps** — Merged 5 GitHub Actions version bumps: `github/codeql-action` v3 to v4, `actions/upload-pages-artifact` v3 to v4, `actions/first-interaction` v1 to v3, `actions/setup-node` v4 to v6, `actions/github-script` v7 to v8.
- **Python dependency refresh** — Bumped `requests` 2.32.3 to 2.33.1, `PyYAML` 6.0.2 to 6.0.3, `jsonschema` 4.23.0 to 4.26.0, `pytest` 8.3.4 to 9.0.3, `pytest-cov` 6.0.0 to 7.1.0, `black` 24.10.0 to 26.3.1, `flake8` 7.1.1 to 7.3.0, `pylint` 3.3.2 to 4.0.5, `mypy` 1.13.0 to 1.20.2, `pip-audit` 2.7.3 to 2.10.0.

## [2.0.0] - 2025-11-23

### Added - Infrastructure & Automation

- **CI/CD Pipeline** (.github/workflows/)
  - Comprehensive validation workflow with markdown linting, link checking, schema validation
  - Automated link health checking (weekly scheduled + PR-triggered)
  - PR auto-labeling and triage workflow
  - Project health tracking with daily GitHub metrics updates
  - Security scanning with Trivy
  - Spell checking with cSpell
  - Duplicate detection and alphabetical ordering validation

- **Security Hardening**
  - CODEOWNERS file for distributed review responsibility
  - Branch protection configuration guide
  - Security policy (SECURITY.md) with vulnerability reporting process
  - Dependabot configuration for automated dependency updates
  - Secret scanning and push protection guidance

- **Validation Scripts** (.github/scripts/)
  - check_alphabetical.py - Validates project ordering within categories
  - check_duplicates.py - Detects duplicate entries and URLs
  - validate_schema.py - Ensures project entry format compliance
  - fetch_project_metrics.py - Collects GitHub stats for all projects
  - generate_badges.py - Creates health badges based on metrics
  - generate_dashboard_data.py - Aggregates ecosystem statistics
  - check_archived_projects.py - Identifies archived/deprecated projects

### Added - Documentation

- **[GETTING-STARTED.md](GETTING-STARTED.md)** - Comprehensive onboarding guide
  - Decision framework for autonomous ops adoption
  - Minimum viable stack recommendations
  - 30-minute quickstart tutorial
  - Common pitfalls and solutions
  - Phased implementation roadmap

- **[GLOSSARY.md](GLOSSARY.md)** - Complete terminology reference
  - 50+ defined terms covering AI, SRE, and autonomous ops concepts
  - Clear explanations of RAG, Graph RAG, MCP, and more
  - Cross-references to other documentation

- **[ARCHITECTURES.md](ARCHITECTURES.md)** - Reference architectures
  - Architecture 1: Read-Only Investigation Assistant
  - Architecture 2: HITL Remediation System
  - Architecture 3: Full Autonomous Platform
  - Security boundaries and deployment patterns
  - Cost optimization strategies

- **[COMPARISONS.md](COMPARISONS.md)** - Tool comparison matrices
  - Side-by-side comparisons for 5 tool categories
  - 20+ comparison attributes per category
  - Recommendations for different use cases
  - Cost comparison analysis

- **[ROADMAP.md](ROADMAP.md)** - Strategic evolution plan
  - Version 2.0: Automation & Community Foundation (current)
  - Version 3.0: Interactive Intelligence Platform (2026)
  - Version 4.0: Collaborative Ecosystem Hub (2027)
  - Detailed features and success metrics for each version

### Added - Community Features

- **GitHub Issue Templates** (.github/ISSUE_TEMPLATE/)
  - new_project.yml - Structured form for project submissions
  - broken_link.yml - Report broken or outdated links
  - case_study.yml - Submit real-world implementation stories
  - improvement.yml - Suggest improvements to the list
  - config.yml - Configure issue template behavior

- **Pull Request Template**
  - Checklist for contributors
  - Project details collection
  - Automated validation reminders

- **Case Study Framework** (case-studies/)
  - README with submission guidelines
  - Comprehensive template for case study submissions
  - Support for multiple anonymization levels
  - Clear benefit articulation for contributors

### Added - GitHub Pages

- **Jekyll Configuration** (_config.yml)
  - GitHub Pages deployment setup
  - SEO optimization
  - Navigation structure
  - Collection configuration for case studies

- **Deployment Workflow** (.github/workflows/pages.yml)
  - Automated Jekyll build and deployment
  - Triggered on push to main branch

- **Gemfile** - Ruby dependencies for Jekyll

### Added - Configuration Files

- **.markdownlint.json** - Markdown style enforcement
- **.github/cspell.json** - Spell checking dictionary with domain terms
- **.github/link-check-config.json** - Link validation configuration

### Changed

- **README.md** - Enhanced structure
  - Added "Getting Started" section with links to new documentation
  - Added "Resources" section organizing documentation and community links
  - Improved navigation with comprehensive table of contents
  - Linked to roadmap and planning documents

### Infrastructure

- Created directory structure:
  - `.github/workflows/` - CI/CD automation
  - `.github/scripts/` - Validation and metrics scripts
  - `.github/ISSUE_TEMPLATE/` - Contribution templates
  - `case-studies/templates/` - Case study templates
  - `data/` - Generated metrics and dashboard data (created by workflows)

## [1.0.0] - 2025-11-22

### Added

- Initial repository structure
- Core curated project list across 6 categories
- Basic README with project descriptions
- CODE_OF_CONDUCT.md
- CONTRIBUTING.md
- LICENSE (MIT)

### Categories Established

- Projects by the Curator
- Graph RAG & Root Cause Analysis for Logs and Incidents
- Agentic Remediation & Runbooks
- MCP Servers & Gateways for Autonomous Ops
- Browser & Desktop Ops Agents
- Compliance, Governance, and Safety for AI Ops
- Datasets, Simulators, and Labs

---

## Upcoming in Version 3.0 (Planned for 2026)

- Semantic search engine with Algolia integration
- Live ecosystem dashboard with real-time metrics
- Interactive tool selector wizard
- User reviews and ratings system
- Certification and badging program
- Automated newsletter and digest
- Advanced analytics and insights

See [ROADMAP.md](ROADMAP.md) for complete future plans.

---

[2.0.0]: https://github.com/nik-kale/awesome-autonomous-ops/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/nik-kale/awesome-autonomous-ops/releases/tag/v1.0.0
