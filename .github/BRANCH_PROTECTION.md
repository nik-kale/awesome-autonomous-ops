# Branch Protection Configuration

This document outlines the required branch protection rules for the `main` branch.

## Required Settings for `main` Branch

Navigate to: **Settings** → **Branches** → **Branch protection rules** → **Add rule**

### Branch name pattern
```
main
```

### Protection Rules

#### Protect matching branches

- ✅ **Require a pull request before merging**
  - ✅ Require approvals: **1**
  - ✅ Dismiss stale pull request approvals when new commits are pushed
  - ✅ Require review from Code Owners
  - ⬜ Restrict who can dismiss pull request reviews (optional)
  - ⬜ Allow specified actors to bypass required pull requests (only for urgent hotfixes)

- ✅ **Require status checks to pass before merging**
  - ✅ Require branches to be up to date before merging
  - Required status checks:
    - `Validate Content & Quality`
    - `Security Scanning`
    - `Check All Links` (for link-check workflow)

- ✅ **Require conversation resolution before merging**
  - All PR comments must be resolved

- ✅ **Require signed commits**
  - Recommended for maintainers (can be optional for contributors)

- ✅ **Require linear history**
  - Prevents merge commits, keeps history clean

- ✅ **Require deployments to succeed before merging**
  - ⬜ (Optional - only if deployment previews are set up)

#### Rules applied to everyone including administrators

- ✅ **Do not allow bypassing the above settings**
- ✅ **Restrict who can push to matching branches**
  - Add: Repository maintainers only
- ✅ **Allow force pushes**: ❌ **DISABLED**
- ✅ **Allow deletions**: ❌ **DISABLED**

### Additional Repository Security Settings

#### General Security

Navigate to: **Settings** → **Security**

- ✅ **Dependency graph**: Enabled (automatic)
- ✅ **Dependabot alerts**: Enabled
- ✅ **Dependabot security updates**: Enabled
- ✅ **Dependabot version updates**: Enabled (via dependabot.yml)

#### Code Security and Analysis

Navigate to: **Settings** → **Code security and analysis**

- ✅ **Secret scanning**: Enabled
- ✅ **Push protection**: Enabled (prevents accidental secret commits)
- ✅ **Secret scanning for non-provider patterns**: Enabled

#### Advanced Security (if available)

- ✅ **Code scanning**: Configure with CodeQL or Trivy
- ✅ **Secret scanning**: Enhanced patterns

### Ruleset Configuration (Alternative/Modern Approach)

GitHub now supports Rulesets as a more flexible alternative to branch protection rules.

Navigate to: **Settings** → **Rules** → **Rulesets** → **New ruleset**

#### Ruleset Details
- **Name**: `main-branch-protection`
- **Enforcement status**: Active
- **Bypass list**: Repository admins (for emergencies only)

#### Target branches
- **Target**: Include by pattern
- **Pattern**: `main`

#### Rules

**Branch Protections:**
- ✅ Restrict deletions
- ✅ Require linear history
- ✅ Require deployments to succeed
- ✅ Require signed commits (recommended)

**Commit Restrictions:**
- ✅ Require a pull request before merging
  - Required approvals: 1
  - Dismiss stale reviews: Yes
  - Require review from CODEOWNERS: Yes

**Status Checks:**
- ✅ Require status checks to pass
  - Required checks:
    - `validate`
    - `security`
    - `link-checker`

**Merge Restrictions:**
- ✅ Block force pushes

### Verification

After configuration, verify by:

1. Attempting to push directly to `main` (should be blocked)
2. Creating a PR without required checks (should not be mergeable)
3. Creating a PR with failed checks (should not be mergeable)
4. Bypassing review as admin (should be prevented if configured)

### Audit

Branch protection settings should be audited:
- **Frequency**: Quarterly
- **Responsibility**: Repository maintainer
- **Checklist**: Verify all checkboxes above remain enabled

---

**Last reviewed**: 2025-11-23
**Next review**: 2026-02-23
