#!/usr/bin/env python3
"""
Check that project entries are in alphabetical order within each category.
"""
import re
import sys
from pathlib import Path


def extract_projects_from_section(content, section_header):
    """Extract project entries from a specific section."""
    # Find the section
    section_pattern = rf'^## {re.escape(section_header)}$(.*?)(?=^## |\Z)'
    section_match = re.search(section_pattern, content, re.MULTILINE | re.DOTALL)

    if not section_match:
        return []

    section_content = section_match.group(1)

    # Extract project entries (lines starting with "- **[")
    project_pattern = r'^- \*\*\[(.*?)\]'
    projects = []

    for match in re.finditer(project_pattern, section_content, re.MULTILINE):
        project_name = match.group(1)
        projects.append(project_name)

    return projects


def check_alphabetical_order(projects, section_name):
    """Check if projects are in alphabetical order."""
    if len(projects) <= 1:
        return True, []

    errors = []
    for i in range(len(projects) - 1):
        current = projects[i].lower()
        next_proj = projects[i + 1].lower()

        if current > next_proj:
            errors.append(f"  ❌ '{projects[i]}' should come after '{projects[i + 1]}'")

    return len(errors) == 0, errors


def main():
    readme_path = Path('README.md')

    if not readme_path.exists():
        print("❌ README.md not found")
        sys.exit(1)

    content = readme_path.read_text()

    # Categories to check (excluding "Projects by the Curator" which has custom ordering)
    categories = [
        'Graph RAG & Root Cause Analysis for Logs and Incidents',
        'Agentic Remediation & Runbooks',
        'MCP Servers & Gateways for Autonomous Ops',
        'Browser & Desktop Ops Agents',
        'Compliance, Governance, and Safety for AI Ops',
        'Datasets, Simulators, and Labs'
    ]

    all_ok = True

    for category in categories:
        projects = extract_projects_from_section(content, category)

        if not projects:
            print(f"⚠️  No projects found in: {category}")
            continue

        is_sorted, errors = check_alphabetical_order(projects, category)

        if is_sorted:
            print(f"✅ {category}: {len(projects)} projects in alphabetical order")
        else:
            print(f"❌ {category}: Not in alphabetical order")
            for error in errors:
                print(error)
            all_ok = False

    if all_ok:
        print("\n✅ All categories are properly sorted!")
        sys.exit(0)
    else:
        print("\n❌ Some categories need alphabetical sorting")
        sys.exit(1)


if __name__ == '__main__':
    main()
