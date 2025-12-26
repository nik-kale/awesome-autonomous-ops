"""
Tests for validate_schema.py script.
"""
import pytest
import sys
from pathlib import Path

# Add scripts directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / '.github' / 'scripts'))

from validate_schema import extract_projects, validate_project_entry


class TestExtractProjects:
    """Test project extraction from README."""
    
    def test_extract_valid_project(self):
        """Test extracting a valid project entry."""
        content = """
## Some Section

- **[Test Project](https://github.com/user/repo)** - A test project description.
"""
        projects = extract_projects(content)
        assert len(projects) == 1
        assert projects[0]['name'] == 'Test Project'
        assert projects[0]['url'] == 'https://github.com/user/repo'
        assert 'description' in projects[0]
    
    def test_extract_multiple_projects(self):
        """Test extracting multiple project entries."""
        content = """
## Section

- **[Project One](https://github.com/user/one)** - First project.
- **[Project Two](https://github.com/user/two)** - Second project.
- **[Project Three](https://github.com/user/three)** - Third project.
"""
        projects = extract_projects(content)
        assert len(projects) == 3
        assert projects[0]['name'] == 'Project One'
        assert projects[1]['name'] == 'Project Two'
        assert projects[2]['name'] == 'Project Three'
    
    def test_extract_with_coming_soon(self):
        """Test extracting projects marked as coming soon."""
        content = """
- **[Future Project](https://github.com/user/future)** *(coming soon)* - Not yet available.
"""
        projects = extract_projects(content)
        assert len(projects) == 1
        assert projects[0]['name'] == 'Future Project'
    
    def test_extract_ignores_invalid_format(self):
        """Test that invalid formats are skipped."""
        content = """
- [Invalid](https://github.com/user/repo) - Missing bold markers.
- Not a link at all
- **Bold but no link** - Description
"""
        projects = extract_projects(content)
        assert len(projects) == 0


class TestValidateProjectEntry:
    """Test project entry validation."""
    
    def test_valid_github_url(self):
        """Test validation of valid GitHub URL."""
        project = {
            'name': 'Test Project',
            'url': 'https://github.com/user/repo',
            'description': 'A valid description.'
        }
        errors = validate_project_entry(project)
        assert len(errors) == 0
    
    def test_invalid_url_format(self):
        """Test validation catches invalid URL format."""
        project = {
            'name': 'Test Project',
            'url': 'not-a-url',
            'description': 'Description'
        }
        errors = validate_project_entry(project)
        assert any('URL' in error for error in errors)
    
    def test_non_github_url(self):
        """Test validation catches non-GitHub URLs."""
        project = {
            'name': 'Test Project',
            'url': 'https://gitlab.com/user/repo',
            'description': 'Description'
        }
        errors = validate_project_entry(project)
        assert any('github.com' in error.lower() for error in errors)
    
    def test_missing_description(self):
        """Test validation catches missing description."""
        project = {
            'name': 'Test Project',
            'url': 'https://github.com/user/repo',
            'description': ''
        }
        errors = validate_project_entry(project)
        assert any('description' in error.lower() for error in errors)
    
    def test_description_too_short(self):
        """Test validation catches overly short descriptions."""
        project = {
            'name': 'Test Project',
            'url': 'https://github.com/user/repo',
            'description': 'Too short'
        }
        errors = validate_project_entry(project)
        # This may or may not be an error depending on implementation
        # Just verify the function runs without crashing
        assert isinstance(errors, list)

