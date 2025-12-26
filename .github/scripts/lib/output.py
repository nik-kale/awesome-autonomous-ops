"""
Consistent output formatting for scripts.
"""
import json
from typing import Any, Dict


# Emoji constants for consistent output
EMOJI_SUCCESS = "✅"
EMOJI_ERROR = "❌"
EMOJI_WARNING = "⚠️"
EMOJI_INFO = "ℹ️"
EMOJI_SEARCH = "🔍"
EMOJI_NEW = "🆕"
EMOJI_STATS = "📊"
EMOJI_ARCHIVE = "🗄️"


def print_success(message: str) -> None:
    """Print success message with emoji."""
    print(f"{EMOJI_SUCCESS} {message}")


def print_error(message: str) -> None:
    """Print error message with emoji."""
    print(f"{EMOJI_ERROR} {message}")


def print_warning(message: str) -> None:
    """Print warning message with emoji."""
    print(f"{EMOJI_WARNING} {message}")


def print_info(message: str) -> None:
    """Print info message with emoji."""
    print(f"{EMOJI_INFO} {message}")


def print_stats(message: str) -> None:
    """Print statistics message with emoji."""
    print(f"{EMOJI_STATS} {message}")


def save_json(data: Dict[str, Any], filepath: str, indent: int = 2) -> None:
    """
    Save data as JSON file.
    
    Args:
        data: Data to save
        filepath: Path to output file
        indent: JSON indentation level
    """
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=indent)


def load_json(filepath: str) -> Dict[str, Any]:
    """
    Load data from JSON file.
    
    Args:
        filepath: Path to JSON file
    
    Returns:
        Loaded data dictionary
    """
    with open(filepath, 'r') as f:
        return json.load(f)

