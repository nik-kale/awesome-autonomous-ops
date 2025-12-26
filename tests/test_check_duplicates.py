"""
Tests for check_duplicates.py script.
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / '.github' / 'scripts'))

from check_duplicates import normalize_url, extract_projects_with_urls


class TestNormalizeUrl:
    """Test URL normalization logic."""
    
    def test_normalize_https_to_http(self):
        """Test normalizing https to http."""
        url = "https://github.com/user/repo"
        normalized = normalize_url(url)
        assert normalized.startswith("http://")
    
    def test_normalize_removes_trailing_slash(self):
        """Test removing trailing slash."""
        url = "https://github.com/user/repo/"
        normalized = normalize_url(url)
        assert not normalized.endswith("/")
    
    def test_normalize_removes_git_extension(self):
        """Test removing .git extension."""
        url = "https://github.com/user/repo.git"
        normalized = normalize_url(url)
        assert not normalized.endswith(".git")
    
    def test_normalize_lowercase(self):
        """Test converting to lowercase."""
        url = "https://github.com/User/Repo"
        normalized = normalize_url(url)
        assert normalized == "http://github.com/user/repo"
    
    def test_normalize_removes_fragments(self):
        """Test removing URL fragments."""
        url = "https://github.com/user/repo#readme"
        normalized = normalize_url(url)
        assert "#" not in normalized
    
    def test_normalize_removes_query_params(self):
        """Test removing query parameters."""
        url = "https://github.com/user/repo?tab=readme"
        normalized = normalize_url(url)
        assert "?" not in normalized
    
    def test_normalize_handles_subpaths(self):
        """Test handling URLs with subpaths."""
        url = "https://github.com/user/repo/tree/main/subdir"
        normalized = normalize_url(url)
        # Should normalize the base part
        assert "github.com/user/repo" in normalized


class TestExtractProjectsWithUrls:
    """Test project extraction with URL tracking."""
    
    def test_extract_single_project(self):
        """Test extracting single project."""
        content = """
- **[Test](https://github.com/user/repo)** - Description.
"""
        projects = extract_projects_with_urls(content)
        assert len(projects) == 1
        assert projects[0]['name'] == 'Test'
        assert 'github.com/user/repo' in projects[0]['url'].lower()
    
    def test_extract_detects_duplicates(self):
        """Test detecting duplicate URLs."""
        content = """
- **[Project A](https://github.com/user/repo)** - First entry.
- **[Project B](https://github.com/user/repo)** - Duplicate URL.
"""
        projects = extract_projects_with_urls(content)
        assert len(projects) == 2
        # Both should have the same normalized URL
        norm1 = normalize_url(projects[0]['url'])
        norm2 = normalize_url(projects[1]['url'])
        assert norm1 == norm2
    
    def test_extract_case_insensitive_duplicates(self):
        """Test detecting duplicates regardless of case."""
        content = """
- **[Project A](https://github.com/User/Repo)** - First.
- **[Project B](https://github.com/user/repo)** - Should be duplicate.
"""
        projects = extract_projects_with_urls(content)
        norm1 = normalize_url(projects[0]['url'])
        norm2 = normalize_url(projects[1]['url'])
        assert norm1 == norm2

