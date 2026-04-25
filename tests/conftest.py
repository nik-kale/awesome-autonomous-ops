"""
Pytest configuration and fixtures for test suite.
"""
import pytest
from pathlib import Path


@pytest.fixture
def sample_readme_content():
    """Provide sample README content for testing."""
    return """
# awesome-autonomous-ops

## Graph RAG & Root Cause Analysis

- **[AutoRCA-Core](https://github.com/nik-kale/AutoRCA-Core)** *(coming soon)* - Graph RAG and multi-signal root cause analysis engine.
- **[LangGraph](https://github.com/langchain-ai/langgraph)** - Framework for building stateful, graph-based AI workflows.
- **[txtai](https://github.com/neuml/txtai)** - Embeddings database for semantic search over logs.

## Agentic Remediation & Runbooks

- **[Kubiya](https://github.com/kubiyabot/community-tools)** - Conversational AI agent for DevOps workflows.
- **[Rundeck](https://github.com/rundeck/rundeck)** - Runbook automation and operational orchestration platform.
"""


@pytest.fixture
def sample_project_metrics():
    """Provide sample project metrics data."""
    return {
        'generated_at': '2024-12-26T00:00:00Z',
        'total_projects': 5,
        'metrics': {
            'user/repo1': {
                'stars': 1000,
                'forks': 200,
                'freshness': 'active',
                'is_archived': False,
                'language': 'Python',
                'license': 'MIT'
            },
            'user/repo2': {
                'stars': 500,
                'forks': 100,
                'freshness': 'moderate',
                'is_archived': False,
                'language': 'Go',
                'license': 'Apache-2.0'
            }
        }
    }


@pytest.fixture
def temp_readme(tmp_path):
    """Create a temporary README file for testing."""
    readme = tmp_path / "README.md"
    readme.write_text("""
# Test Repository

## Test Section

- **[Project A](https://github.com/user/projecta)** - First project.
- **[Project B](https://github.com/user/projectb)** - Second project.
""")
    return readme

