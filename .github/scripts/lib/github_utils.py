"""
GitHub URL parsing and API utilities.
"""
import re
from typing import Tuple, Optional


def parse_github_url(url: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Parse GitHub URL to extract owner and repo.
    
    Args:
        url: GitHub URL (e.g., https://github.com/owner/repo)
    
    Returns:
        Tuple of (owner, repo) or (None, None) if invalid
    """
    # Handle URLs like: https://github.com/owner/repo or https://github.com/owner/repo/tree/main/...
    pattern = r'github\.com/([^/]+)/([^/]+)'
    match = re.search(pattern, url)
    
    if match:
        owner = match.group(1)
        repo = match.group(2)
        # Remove .git extension if present
        repo = repo.replace('.git', '')
        return owner, repo
    
    return None, None


def normalize_github_url(url: str) -> str:
    """
    Normalize GitHub URL for comparison (lowercase, remove trailing slash, etc.).
    
    Args:
        url: GitHub URL
    
    Returns:
        Normalized URL string
    """
    # Convert to lowercase
    url = url.lower()
    
    # Convert https to http for comparison
    url = url.replace('https://', 'http://')
    
    # Remove trailing slash
    url = url.rstrip('/')
    
    # Remove .git extension
    url = url.replace('.git', '')
    
    # Remove URL fragments and query params
    url = re.sub(r'[#?].*$', '', url)
    
    return url


def is_github_url(url: str) -> bool:
    """
    Check if URL is a GitHub URL.
    
    Args:
        url: URL to check
    
    Returns:
        True if GitHub URL, False otherwise
    """
    return 'github.com' in url.lower()

