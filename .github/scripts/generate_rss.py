#!/usr/bin/env python3
"""
Generate RSS feed for new project additions.
"""
import json
import re
from pathlib import Path
from datetime import datetime, timezone
from email.utils import format_datetime


def extract_projects_by_section(content):
    """Extract all projects organized by section."""
    projects_by_section = {}
    current_section = None
    
    # Pattern for section headers (## Section Name)
    section_pattern = r'^##\s+(.+)$'
    # Pattern for project entries
    project_pattern = r'^\- \*\*\[(.*?)\]\((https://github\.com/[^)]+)\)\*\*(?:\s*\*\(coming soon\)\*)?\s*[-–]\s*(.+)$'
    
    for line in content.split('\n'):
        # Check for section header
        section_match = re.match(section_pattern, line)
        if section_match:
            current_section = section_match.group(1).strip()
            if current_section not in projects_by_section:
                projects_by_section[current_section] = []
            continue
        
        # Check for project entry
        if current_section:
            project_match = re.match(project_pattern, line)
            if project_match:
                name = project_match.group(1)
                url = project_match.group(2)
                description = project_match.group(3).strip()
                
                projects_by_section[current_section].append({
                    'name': name,
                    'url': url,
                    'description': description,
                    'category': current_section
                })
    
    return projects_by_section


def load_previous_projects():
    """Load previously tracked projects from JSON."""
    projects_file = Path('data/tracked-projects.json')
    
    if not projects_file.exists():
        return set()
    
    try:
        with open(projects_file, 'r') as f:
            data = json.load(f)
            return set(data.get('project_urls', []))
    except Exception as e:
        print(f"⚠️  Error loading previous projects: {e}")
        return set()


def save_tracked_projects(project_urls):
    """Save current project URLs for next run."""
    output_dir = Path('data')
    output_dir.mkdir(exist_ok=True)
    
    projects_file = output_dir / 'tracked-projects.json'
    
    with open(projects_file, 'w') as f:
        json.dump({
            'updated_at': datetime.now(timezone.utc).isoformat(),
            'project_urls': list(project_urls)
        }, f, indent=2)


def generate_rss_feed(new_projects, all_projects_by_section):
    """Generate RSS 2.0 feed XML."""
    now = datetime.now(timezone.utc)
    
    xml = ['<?xml version="1.0" encoding="UTF-8" ?>']
    xml.append('<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">')
    xml.append('  <channel>')
    xml.append('    <title>Awesome Autonomous Operations - New Projects</title>')
    xml.append('    <link>https://github.com/nik-kale/awesome-autonomous-ops</link>')
    xml.append('    <description>New additions to the Awesome Autonomous Operations curated list</description>')
    xml.append('    <language>en-us</language>')
    xml.append(f'    <lastBuildDate>{format_datetime(now)}</lastBuildDate>')
    xml.append('    <atom:link href="https://raw.githubusercontent.com/nik-kale/awesome-autonomous-ops/main/feed.xml" rel="self" type="application/rss+xml" />')
    
    # Add items for new projects (most recent first)
    for project_url in sorted(new_projects, reverse=True):
        # Find project details
        project_data = None
        for section, projects in all_projects_by_section.items():
            for proj in projects:
                if proj['url'] == project_url:
                    project_data = proj
                    break
            if project_data:
                break
        
        if not project_data:
            continue
        
        xml.append('    <item>')
        xml.append(f'      <title>{escape_xml(project_data["name"])} - {escape_xml(project_data["category"])}</title>')
        xml.append(f'      <link>{escape_xml(project_data["url"])}</link>')
        xml.append(f'      <guid isPermaLink="true">{escape_xml(project_data["url"])}</guid>')
        xml.append(f'      <pubDate>{format_datetime(now)}</pubDate>')
        xml.append(f'      <category>{escape_xml(project_data["category"])}</category>')
        
        description = f'{escape_xml(project_data["description"])}<br/><br/>'
        description += f'Category: {escape_xml(project_data["category"])}<br/>'
        description += f'<a href="{escape_xml(project_data["url"])}">{escape_xml(project_data["url"])}</a>'
        
        xml.append(f'      <description>{description}</description>')
        xml.append('    </item>')
    
    xml.append('  </channel>')
    xml.append('</rss>')
    
    return '\n'.join(xml)


def escape_xml(text):
    """Escape special XML characters."""
    if not text:
        return ''
    
    text = str(text)
    text = text.replace('&', '&amp;')
    text = text.replace('<', '&lt;')
    text = text.replace('>', '&gt;')
    text = text.replace('"', '&quot;')
    text = text.replace("'", '&apos;')
    return text


def main():
    readme_path = Path('README.md')
    
    if not readme_path.exists():
        print("❌ README.md not found")
        return
    
    # Parse current README
    content = readme_path.read_text()
    all_projects_by_section = extract_projects_by_section(content)
    
    # Get all current project URLs
    current_urls = set()
    for section, projects in all_projects_by_section.items():
        for proj in projects:
            current_urls.add(proj['url'])
    
    print(f"📊 Found {len(current_urls)} total projects")
    
    # Load previously tracked projects
    previous_urls = load_previous_projects()
    
    # Find new projects
    new_projects = current_urls - previous_urls
    
    if new_projects:
        print(f"🆕 Found {len(new_projects)} new project(s):")
        for url in sorted(new_projects):
            print(f"  - {url}")
    else:
        print("ℹ️  No new projects since last run")
    
    # Generate RSS feed
    rss_xml = generate_rss_feed(new_projects, all_projects_by_section)
    
    # Save feed
    feed_path = Path('feed.xml')
    feed_path.write_text(rss_xml)
    print(f"✅ RSS feed saved to {feed_path}")
    
    # Update tracked projects
    save_tracked_projects(current_urls)
    print(f"✅ Updated tracked projects list")


if __name__ == '__main__':
    main()

