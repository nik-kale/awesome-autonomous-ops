"""
Tests for check_alphabetical.py script.
"""
import pytest
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent / '.github' / 'scripts'))

from check_alphabetical import extract_sections, check_section_order


class TestExtractSections:
    """Test section extraction from README."""

    def test_extract_simple_section(self):
        """Test extracting a simple section with projects."""
        content = """
## Test Section

- **[Alpha](https://github.com/user/alpha)** - First.
- **[Beta](https://github.com/user/beta)** - Second.
"""
        sections = extract_sections(content)
        assert 'Test Section' in sections
        assert len(sections['Test Section']) == 2
        assert sections['Test Section'][0]['name'] == 'Alpha'
        assert sections['Test Section'][1]['name'] == 'Beta'

    def test_extract_multiple_sections(self):
        """Test extracting multiple sections."""
        content = """
## Section One

- **[ProjectA](https://github.com/user/a)** - Description.

## Section Two

- **[ProjectB](https://github.com/user/b)** - Description.
- **[ProjectC](https://github.com/user/c)** - Description.
"""
        sections = extract_sections(content)
        assert len(sections) == 2
        assert 'Section One' in sections
        assert 'Section Two' in sections
        assert len(sections['Section One']) == 1
        assert len(sections['Section Two']) == 2

    def test_extract_ignores_non_project_lines(self):
        """Test that non-project lines are ignored."""
        content = """
## Test Section

Some introductory text here.

- **[Project](https://github.com/user/proj)** - Description.

More text here.
"""
        sections = extract_sections(content)
        assert len(sections['Test Section']) == 1


class TestCheckSectionOrder:
    """Test alphabetical ordering check."""

    def test_alphabetical_order_valid(self):
        """Test correctly ordered projects pass validation."""
        projects = [
            {'name': 'Alpha', 'line': 10},
            {'name': 'Beta', 'line': 11},
            {'name': 'Gamma', 'line': 12}
        ]
        errors = check_section_order('Test Section', projects)
        assert len(errors) == 0

    def test_alphabetical_order_invalid(self):
        """Test incorrectly ordered projects are caught."""
        projects = [
            {'name': 'Beta', 'line': 10},
            {'name': 'Alpha', 'line': 11},  # Out of order
            {'name': 'Gamma', 'line': 12}
        ]
        errors = check_section_order('Test Section', projects)
        assert len(errors) > 0
        assert 'Alpha' in errors[0] or 'Beta' in errors[0]

    def test_case_insensitive_ordering(self):
        """Test that ordering is case-insensitive."""
        projects = [
            {'name': 'alpha', 'line': 10},
            {'name': 'Beta', 'line': 11},
            {'name': 'GAMMA', 'line': 12}
        ]
        errors = check_section_order('Test Section', projects)
        assert len(errors) == 0

    def test_special_characters_in_names(self):
        """Test handling of special characters in project names."""
        projects = [
            {'name': 'A-Project', 'line': 10},
            {'name': 'B_Project', 'line': 11},
            {'name': 'C Project', 'line': 12}
        ]
        errors = check_section_order('Test Section', projects)
        # Should handle gracefully without crashing
        assert isinstance(errors, list)

    def test_numbers_in_names(self):
        """Test handling of numbers in project names."""
        projects = [
            {'name': '2FA Tool', 'line': 10},
            {'name': 'Alpha', 'line': 11},
            {'name': 'Beta-2', 'line': 12}
        ]
        errors = check_section_order('Test Section', projects)
        # May or may not be errors depending on sorting logic
        assert isinstance(errors, list)

