#!/usr/bin/env python3
"""
Check for archived projects and create alerts.
"""
import json
from pathlib import Path


def main():
    metrics_file = Path('data/project-metrics.json')

    if not metrics_file.exists():
        print("⚠️  No metrics file found")
        return

    with open(metrics_file) as f:
        data = json.load(f)

    metrics = data['metrics']
    archived = []

    for repo, repo_data in metrics.items():
        if isinstance(repo_data, dict) and repo_data.get('is_archived', False):
            archived.append({
                'repo': repo,
                'updated_at': repo_data.get('updated_at', 'unknown')
            })

    if archived:
        print(f"🗄️  Found {len(archived)} archived projects:")
        for proj in archived:
            print(f"  - {proj['repo']}")

        # Save for workflow to create issue
        output_file = Path('data/archived-projects.json')
        with open(output_file, 'w') as f:
            json.dump(archived, f, indent=2)
    else:
        print("✅ No archived projects detected")

        # Remove the file if it exists
        archived_file = Path('data/archived-projects.json')
        if archived_file.exists():
            archived_file.unlink()


if __name__ == '__main__':
    main()
