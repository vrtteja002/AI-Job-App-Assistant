"""
This module contains Streamlit-specific code for the AI Job Application Assistant.
"""

from stream.app import run_streamlit_app
from stream.helpers import display_application_statistics, display_job_match_score

__all__ = [
    'run_streamlit_app',
    'display_application_statistics',
    'display_job_match_score'
]
