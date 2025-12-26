"""
Tests for fetch_project_metrics.py script.
"""
import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).parent.parent / '.github' / 'scripts'))

from fetch_project_metrics import extract_github_projects, parse_github_url


class TestExtractGithubProjects:
    """Test GitHub project extraction."""

    def test_extract_single_project(self):
        """Test extracting a single GitHub project."""
        content = """
- **[Test Project](https://github.com/user/repo)** - Description.
"""
        projects = extract_github_projects(content)
        assert len(projects) == 1
        assert projects[0]['name'] == 'Test Project'
        assert projects[0]['url'] == 'https://github.com/user/repo'

    def test_extract_multiple_projects(self):
        """Test extracting multiple GitHub projects."""
        content = """
- **[Project A](https://github.com/user/repoa)** - First.
- **[Project B](https://github.com/user/repob)** - Second.
- **[Project C](https://github.com/other/repoc)** - Third.
"""
        projects = extract_github_projects(content)
        assert len(projects) == 3

    def test_extract_ignores_non_github(self):
        """Test that non-GitHub URLs are ignored."""
        content = """
- **[GitHub Project](https://github.com/user/repo)** - Valid.
- **[GitLab Project](https://gitlab.com/user/repo)** - Ignored.
- **[Other Site](https://example.com)** - Ignored.
"""
        projects = extract_github_projects(content)
        assert len(projects) == 1
        assert 'github.com' in projects[0]['url']

    def test_extract_with_subpaths(self):
        """Test extracting URLs with subpaths."""
        content = """
- **[Subdir Project](https://github.com/user/repo/tree/main/subdir)** - Has subpath.
"""
        projects = extract_github_projects(content)
        assert len(projects) == 1
        assert 'github.com/user/repo' in projects[0]['url']


class TestParseGithubUrl:
    """Test GitHub URL parsing."""

    def test_parse_simple_url(self):
        """Test parsing a simple GitHub URL."""
        url = "https://github.com/user/repo"
        owner, repo = parse_github_url(url)
        assert owner == "user"
        assert repo == "repo"

    def test_parse_url_with_subpath(self):
        """Test parsing URL with subpath."""
        url = "https://github.com/owner/repository/tree/main/src"
        owner, repo = parse_github_url(url)
        assert owner == "owner"
        assert repo == "repository"

    def test_parse_url_with_trailing_slash(self):
        """Test parsing URL with trailing slash."""
        url = "https://github.com/user/repo/"
        owner, repo = parse_github_url(url)
        assert owner == "user"
        assert repo == "repo"

    def test_parse_url_with_git_extension(self):
        """Test parsing URL with .git extension."""
        url = "https://github.com/user/repo.git"
        owner, repo = parse_github_url(url)
        assert owner == "user"
        assert repo == "repo"

    def test_parse_invalid_url(self):
        """Test parsing invalid URL returns None."""
        url = "https://example.com/not/github"
        owner, repo = parse_github_url(url)
        assert owner is None
        assert repo is None

    def test_parse_malformed_url(self):
        """Test parsing malformed URL."""
        url = "not-a-url"
        owner, repo = parse_github_url(url)
        assert owner is None
        assert repo is None


class TestFetchRepoMetrics:
    """Test repository metrics fetching (mocked)."""

    @patch('fetch_project_metrics.requests.get')
    def test_fetch_metrics_success(self, mock_get):
        """Test successful metrics fetch."""
        from fetch_project_metrics import fetch_repo_metrics

        # Mock successful API response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            'stargazers_count': 100,
            'forks_count': 50,
            'open_issues_count': 10,
            'watchers_count': 100,
            'updated_at': '2024-12-20T00:00:00Z',
            'created_at': '2023-01-01T00:00:00Z',
            'archived': False,
            'license': {'spdx_id': 'MIT'},
            'language': 'Python',
            'description': 'Test repository'
        }
        mock_get.return_value = mock_response

        metrics = fetch_repo_metrics('user', 'repo', 'fake-token')

        assert metrics['stars'] == 100
        assert metrics['forks'] == 50
        assert metrics['is_archived'] is False
        assert metrics['license'] == 'MIT'
        assert metrics['language'] == 'Python'

    @patch('fetch_project_metrics.requests.get')
    def test_fetch_metrics_not_found(self, mock_get):
        """Test handling of 404 response."""
        from fetch_project_metrics import fetch_repo_metrics

        mock_response = Mock()
        mock_response.status_code = 404
        mock_get.return_value = mock_response

        metrics = fetch_repo_metrics('user', 'nonexistent', 'fake-token')

        assert 'error' in metrics
        assert metrics['error'] == 'not_found'

    @patch('fetch_project_metrics.requests.get')
    def test_fetch_metrics_rate_limited(self, mock_get):
        """Test handling of rate limit response."""
        from fetch_project_metrics import fetch_repo_metrics

        mock_response = Mock()
        mock_response.status_code = 403
        mock_get.return_value = mock_response

        metrics = fetch_repo_metrics('user', 'repo', 'fake-token')

        assert 'error' in metrics
        assert metrics['error'] == 'rate_limited'

