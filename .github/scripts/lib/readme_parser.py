"""
README parsing utilities for extracting project information.
"""
import re
from typing import List, Dict


def extract_github_projects(content: str) -> List[Dict[str, str]]:
    """
    Extract GitHub project URLs from README content.
    
    Args:
        content: README markdown content
    
    Returns:
        List of dictionaries with 'name' and 'url' keys
    """
    pattern = r'^\- \*\*\[(.*?)\]\((https://github\.com/[^)]+)\)\*\*'
    projects = []
    
    for match in re.finditer(pattern, content, re.MULTILINE):
        name = match.group(1)
        url = match.group(2)
        projects.append({'name': name, 'url': url})
    
    return projects


def extract_projects_with_descriptions(content: str) -> List[Dict[str, str]]:
    """
    Extract projects with their descriptions from README.
    
    Args:
        content: README markdown content
    
    Returns:
        List of dictionaries with 'name', 'url', and 'description' keys
    """
    pattern = r'^\- \*\*\[(.*?)\]\((https://github\.com/[^)]+)\)\*\*(?:\s*\*\(coming soon\)\*)?\s*[-–]\s*(.+)$'
    projects = []
    
    for match in re.finditer(pattern, content, re.MULTILINE):
        name = match.group(1)
        url = match.group(2)
        description = match.group(3).strip()
        
        projects.append({
            'name': name,
            'url': url,
            'description': description
        })
    
    return projects


def extract_projects_by_section(content: str) -> Dict[str, List[Dict[str, str]]]:
    """
    Extract projects organized by section headers.
    
    Args:
        content: README markdown content
    
    Returns:
        Dictionary mapping section names to lists of projects
    """
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

