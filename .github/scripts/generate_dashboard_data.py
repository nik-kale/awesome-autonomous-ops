#!/usr/bin/env python3
"""
Generate dashboard data for ecosystem visualization.
"""
import json
from pathlib import Path
from collections import Counter


def main():
    metrics_file = Path('data/project-metrics.json')

    if not metrics_file.exists():
        print("⚠️  No metrics file found")
        return

    with open(metrics_file) as f:
        data = json.load(f)

    metrics = data['metrics']

    # Aggregate statistics
    freshness_dist = Counter()
    language_dist = Counter()
    license_dist = Counter()

    total_stars = 0
    total_forks = 0

    for repo, repo_data in metrics.items():
        if isinstance(repo_data, dict) and 'error' not in repo_data:
            freshness_dist[repo_data.get('freshness', 'unknown')] += 1
            language_dist[repo_data.get('language', 'Unknown')] += 1
            license_dist[repo_data.get('license', 'Unknown')] += 1
            total_stars += repo_data.get('stars', 0)
            total_forks += repo_data.get('forks', 0)

    dashboard_data = {
        'generated_at': data['generated_at'],
        'overview': {
            'total_projects': data['total_projects'],
            'total_stars': total_stars,
            'total_forks': total_forks
        },
        'freshness_distribution': dict(freshness_dist),
        'top_languages': dict(language_dist.most_common(10)),
        'license_distribution': dict(license_dist.most_common(10))
    }

    output_file = Path('data/dashboard-data.json')
    with open(output_file, 'w') as f:
        json.dump(dashboard_data, f, indent=2)

    print(f"✅ Dashboard data saved to {output_file}")
    print(f"📊 Total stars across ecosystem: {total_stars:,}")
    print(f"📊 Total forks across ecosystem: {total_forks:,}")


if __name__ == '__main__':
    main()
