"""
This module makes utility functions available throughout the application.
It imports both the base utility functions and any helper modules.
"""

# Import utility functions from the main utils file
from utils.helpers import (
    validate_json_response,
    format_date,
    ensure_directory_exists,
    save_text_to_file,
    read_text_from_file,
    extract_keywords,
    similarity_score,
    get_file_extension,
    sanitize_filename,
    truncate_text
)

# Add any specialized utility modules here if needed
# from utils.specialized_module import specific_function

__all__ = [
    'validate_json_response',
    'format_date',
    'ensure_directory_exists',
    'save_text_to_file',
    'read_text_from_file',
    'extract_keywords',
    'similarity_score',
    'get_file_extension',
    'sanitize_filename',
    'truncate_text'
]
