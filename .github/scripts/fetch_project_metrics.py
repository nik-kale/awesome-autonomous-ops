#!/usr/bin/env python3
"""
Fetch GitHub metrics for all projects in README.md.
"""
import json
import os
import re
import sys
import time
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    print("Installing requests...")
    os.system("pip install requests")
    import requests


def extract_github_projects(content):
    """Extract GitHub project URLs from README."""
    pattern = r'^- \*\*\[(.*?)\]\((https://github\.com/[^)]+)\)\*\*'
    projects = []

    for match in re.finditer(pattern, content, re.MULTILINE):
        name = match.group(1)
        url = match.group(2)
        projects.append({'name': name, 'url': url})

    return projects


def parse_github_url(url):
    """Parse GitHub URL to extract owner and repo."""
    # Handle URLs like: https://github.com/owner/repo or https://github.com/owner/repo/tree/main/...
    pattern = r'github\.com/([^/]+)/([^/]+)'
    match = re.search(pattern, url)

    if match:
        owner = match.group(1)
        repo = match.group(2)
        return owner, repo

    return None, None


def fetch_repo_metrics(owner, repo, token):
    """Fetch metrics for a single repository."""
    headers = {}
    if token:
        headers['Authorization'] = f'token {token}'
        headers['Accept'] = 'application/vnd.github.v3+json'

    try:
        url = f'https://api.github.com/repos/{owner}/{repo}'
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 404:
            return {'error': 'not_found'}
        elif response.status_code == 403:
            return {'error': 'rate_limited'}
        elif response.status_code != 200:
            return {'error': f'http_{response.status_code}'}

        data = response.json()

        # Calculate days since last update
        updated_at = datetime.fromisoformat(data['updated_at'].replace('Z', '+00:00'))
        days_since_update = (datetime.now(timezone.utc) - updated_at).days

        # Determine freshness
        if days_since_update < 90:
            freshness = 'active'  # 🟢
        elif days_since_update < 365:
            freshness = 'moderate'  # 🟡
        elif days_since_update < 730:
            freshness = 'stale'  # 🟠
        else:
            freshness = 'inactive'  # 🔴

        return {
            'stars': data['stargazers_count'],
            'forks': data['forks_count'],
            'open_issues': data['open_issues_count'],
            'watchers': data['watchers_count'],
            'updated_at': data['updated_at'],
            'created_at': data['created_at'],
            'days_since_update': days_since_update,
            'freshness': freshness,
            'is_archived': data['archived'],
            'license': data.get('license', {}).get('spdx_id', 'Unknown') if data.get('license') else 'Unknown',
            'language': data.get('language', 'Unknown'),
            'description': data.get('description', '')
        }

    except Exception as e:
        return {'error': str(e)}


def main():
    readme_path = Path('README.md')

    if not readme_path.exists():
        print("❌ README.md not found")
        sys.exit(1)

    content = readme_path.read_text()
    projects = extract_github_projects(content)

    print(f"📊 Found {len(projects)} GitHub projects")

    token = os.environ.get('GITHUB_TOKEN')
    if not token:
        print("⚠️  No GITHUB_TOKEN found - rate limiting may occur")

    metrics = {}
    archived = []

    for i, project in enumerate(projects, 1):
        owner, repo = parse_github_url(project['url'])

        if not owner or not repo:
            print(f"  [{i}/{len(projects)}] ⚠️  Skipping {project['name']}: Invalid URL")
            continue

        print(f"  [{i}/{len(projects)}] Fetching metrics for {owner}/{repo}...")

        repo_metrics = fetch_repo_metrics(owner, repo, token)

        if 'error' in repo_metrics:
            print(f"    ❌ Error: {repo_metrics['error']}")
        else:
            freshness_emoji = {
                'active': '🟢',
                'moderate': '🟡',
                'stale': '🟠',
                'inactive': '🔴'
            }
            emoji = freshness_emoji.get(repo_metrics['freshness'], '⚪')
            print(f"    {emoji} Stars: {repo_metrics['stars']}, Last update: {repo_metrics['days_since_update']} days ago")

            if repo_metrics['is_archived']:
                archived.append({
                    'name': project['name'],
                    'url': project['url'],
                    'archived_at': repo_metrics['updated_at']
                })

        metrics[f"{owner}/{repo}"] = repo_metrics

        # Rate limiting: wait between requests
        if (i % 10) == 0:
            time.sleep(1)

    # Save metrics
    output_dir = Path('data')
    output_dir.mkdir(exist_ok=True)

    metrics_file = output_dir / 'project-metrics.json'
    with open(metrics_file, 'w') as f:
        json.dump({
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'total_projects': len(projects),
            'metrics': metrics
        }, f, indent=2)

    print(f"\n✅ Metrics saved to {metrics_file}")

    # Save archived projects if any
    if archived:
        archived_file = output_dir / 'archived-projects.json'
        with open(archived_file, 'w') as f:
            json.dump(archived, f, indent=2)
        print(f"⚠️  {len(archived)} archived projects saved to {archived_file}")


if __name__ == '__main__':
    main()
