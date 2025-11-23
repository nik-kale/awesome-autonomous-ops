#!/usr/bin/env python3
"""
Generate health badges based on project metrics.
"""
import json
from pathlib import Path


def generate_badge_markdown(label, message, color):
    """Generate shields.io badge markdown."""
    return f"![{label}](https://img.shields.io/badge/{label}-{message}-{color})"


def get_freshness_badge(days):
    """Get freshness badge based on days since last update."""
    if days < 90:
        return generate_badge_markdown("freshness", "active", "brightgreen")
    elif days < 365:
        return generate_badge_markdown("freshness", "moderate", "yellow")
    elif days < 730:
        return generate_badge_markdown("freshness", "stale", "orange")
    else:
        return generate_badge_markdown("freshness", "inactive", "red")


def main():
    metrics_file = Path('data/project-metrics.json')

    if not metrics_file.exists():
        print("⚠️  No metrics file found")
        return

    with open(metrics_file) as f:
        data = json.load(f)

    metrics = data['metrics']

    # Generate aggregate statistics
    total = len(metrics)
    active = sum(1 for m in metrics.values() if not isinstance(m, dict) or m.get('freshness') == 'active')
    archived = sum(1 for m in metrics.values() if isinstance(m, dict) and m.get('is_archived', False))

    print(f"📊 Total projects: {total}")
    print(f"🟢 Active projects: {active}")
    print(f"🗄️  Archived projects: {archived}")

    # Save badge data
    badge_data = {
        'total': total,
        'active': active,
        'archived': archived,
        'active_percentage': round((active / total * 100) if total > 0 else 0, 1)
    }

    output_file = Path('data/badge-data.json')
    with open(output_file, 'w') as f:
        json.dump(badge_data, f, indent=2)

    print(f"✅ Badge data saved to {output_file}")


if __name__ == '__main__':
    main()
