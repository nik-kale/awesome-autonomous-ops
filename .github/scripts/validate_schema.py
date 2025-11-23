#!/usr/bin/env python3
"""
Validate project entries against schema requirements.
"""
import re
import sys
from pathlib import Path


def validate_entry_format(line, line_num):
    """Validate a single project entry."""
    errors = []

    # Expected format: - **[Name](URL)** – Description
    pattern = r'^- \*\*\[(.*?)\]\((.*?)\)\*\* – (.+)$'
    match = re.match(pattern, line)

    if not match:
        errors.append(f"Line {line_num}: Invalid format")
        return errors

    name, url, description = match.groups()

    # Validate name
    if len(name.strip()) == 0:
        errors.append(f"Line {line_num}: Empty project name")

    # Validate URL
    if not url.startswith('http'):
        errors.append(f"Line {line_num}: URL must start with http:// or https://")

    if url.startswith('http://') and 'localhost' not in url:
        errors.append(f"Line {line_num}: Use HTTPS instead of HTTP for '{name}'")

    # Validate description
    desc_len = len(description.strip())
    if desc_len < 10:
        errors.append(f"Line {line_num}: Description too short ({desc_len} chars) for '{name}'")
    elif desc_len > 250:
        errors.append(f"Line {line_num}: Description too long ({desc_len} chars) for '{name}'")

    # Check description ends with period
    if not description.strip().endswith('.'):
        errors.append(f"Line {line_num}: Description should end with period for '{name}'")

    return errors


def main():
    readme_path = Path('README.md')

    if not readme_path.exists():
        print("❌ README.md not found")
        sys.exit(1)

    content = readme_path.read_text()
    lines = content.split('\n')

    all_errors = []
    entry_count = 0

    for i, line in enumerate(lines, 1):
        # Check if this is a project entry
        if line.startswith('- **['):
            entry_count += 1
            errors = validate_entry_format(line, i)
            all_errors.extend(errors)

    print(f"📊 Validated {entry_count} project entries")

    if not all_errors:
        print("✅ All entries pass schema validation!")
        sys.exit(0)

    print(f"\n❌ Found {len(all_errors)} validation error(s):\n")
    for error in all_errors:
        print(f"  {error}")

    # Don't fail CI for now, just warn
    sys.exit(0)


if __name__ == '__main__':
    main()
