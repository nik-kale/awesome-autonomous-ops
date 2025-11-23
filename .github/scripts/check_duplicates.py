#!/usr/bin/env python3
"""
Check for duplicate project entries in README.md.
"""
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


def normalize_url(url):
    """Normalize URL for comparison."""
    parsed = urlparse(url)
    # Remove trailing slashes, convert to lowercase
    path = parsed.path.rstrip('/').lower()
    return f"{parsed.netloc.lower()}{path}"


def extract_all_projects(content):
    """Extract all project entries from README."""
    # Pattern: - **[Name](URL)** – Description
    pattern = r'^- \*\*\[(.*?)\]\((.*?)\)\*\*'
    projects = []

    for match in re.finditer(pattern, content, re.MULTILINE):
        name = match.group(1).strip()
        url = match.group(2).strip()
        projects.append({
            'name': name,
            'url': url,
            'normalized_url': normalize_url(url),
            'line': content[:match.start()].count('\n') + 1
        })

    return projects


def check_duplicates(projects):
    """Check for duplicate names and URLs."""
    seen_names = {}
    seen_urls = {}
    duplicates = []

    for project in projects:
        name = project['name'].lower()
        norm_url = project['normalized_url']

        # Check duplicate names
        if name in seen_names:
            duplicates.append({
                'type': 'name',
                'value': project['name'],
                'line1': seen_names[name],
                'line2': project['line']
            })
        else:
            seen_names[name] = project['line']

        # Check duplicate URLs
        if norm_url in seen_urls:
            duplicates.append({
                'type': 'url',
                'value': project['url'],
                'line1': seen_urls[norm_url],
                'line2': project['line']
            })
        else:
            seen_urls[norm_url] = project['line']

    return duplicates


def main():
    readme_path = Path('README.md')

    if not readme_path.exists():
        print("❌ README.md not found")
        sys.exit(1)

    content = readme_path.read_text()
    projects = extract_all_projects(content)

    print(f"📊 Found {len(projects)} total project entries")

    duplicates = check_duplicates(projects)

    if not duplicates:
        print("✅ No duplicate projects found!")
        sys.exit(0)

    print(f"\n❌ Found {len(duplicates)} duplicate(s):\n")

    for dup in duplicates:
        if dup['type'] == 'name':
            print(f"  Duplicate project name: '{dup['value']}'")
        else:
            print(f"  Duplicate URL: '{dup['value']}'")
        print(f"    - Line {dup['line1']}")
        print(f"    - Line {dup['line2']}")
        print()

    sys.exit(1)


if __name__ == '__main__':
    main()
