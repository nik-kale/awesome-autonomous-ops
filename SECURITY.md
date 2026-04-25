# Security Policy

## Reporting Security Issues

The security of awesome-autonomous-ops is important to us. If you discover a security vulnerability, please report it responsibly.

### Reporting Process

**DO NOT** open a public GitHub issue for security vulnerabilities.

Instead, please report security issues via:

1. **GitHub Security Advisories**: Use the [Security tab](https://github.com/nik-kale/awesome-autonomous-ops/security/advisories/new) to privately report vulnerabilities
2. **Email**: Contact the maintainer directly (see profile for contact information)

### What to Include

When reporting a security issue, please include:

- Description of the vulnerability
- Steps to reproduce the issue
- Potential impact
- Suggested fix (if you have one)

### Response Timeline

- **Initial Response**: Within 48 hours
- **Status Update**: Within 7 days
- **Fix Timeline**: Varies based on severity (critical issues prioritized)

## Scope

This security policy covers:

1. **Malicious Links**: Detection and removal of malicious URLs in project submissions
2. **Content Injection**: Prevention of XSS or malicious markdown injection
3. **Automation Security**: GitHub Actions workflows, scripts, and CI/CD pipeline security
4. **Access Control**: Repository permissions and branch protection

## Security Measures

### Current Protections

- ✅ Automated link validation (malicious link detection)
- ✅ HTTPS enforcement for all external links
- ✅ Content Security Policy (CSP) on GitHub Pages
- ✅ Branch protection on main branch
- ✅ Required PR reviews before merge
- ✅ Automated security scanning (Trivy)
- ✅ GitHub Actions security best practices
- ✅ Secrets scanning enabled
- ✅ Dependabot security updates

### Link Security

All submitted URLs are:

1. Scanned for HTTPS compliance
2. Validated against known malicious domain lists
3. Checked for typosquatting patterns
4. Verified to match claimed projects (GitHub API validation)

### Content Security

- Markdown files are sanitized before rendering
- Raw HTML is disallowed in submissions
- Script tags are automatically detected and rejected
- User-generated content undergoes automated validation

### Access Control

- Main branch requires PR review
- Force pushes are prevented
- Commit signing is encouraged for maintainers
- CODEOWNERS file defines review requirements

## Responsible Disclosure

We follow responsible disclosure practices:

1. Security issues are addressed privately
2. Fixes are developed and tested before public disclosure
3. Credit is given to reporters (unless anonymity is requested)
4. Public advisory is published after fix is deployed

## Dependencies

This repository has minimal dependencies (primarily GitHub Actions). All dependencies are:

- Pinned to specific versions or commit SHAs
- Monitored by Dependabot
- Automatically updated for security patches
- Reviewed before merging

## Security Best Practices for Contributors

When contributing:

- ✅ Use HTTPS URLs only
- ✅ Verify project authenticity before submission
- ✅ Avoid submitting archived or unmaintained projects
- ✅ Report suspicious projects or links immediately
- ✅ Follow markdown formatting guidelines (no raw HTML)
- ✅ Sign your commits with GPG (recommended)

## Security Audit History

- **2025-11**: Initial security policy established
- **2025-11**: Automated security scanning implemented
- **2025-11**: Branch protection and access controls configured

## Contact

For security concerns, contact: @nik-kale via GitHub

---

Last updated: 2025-11-23
