"""
This module initializes the pages package containing all Streamlit page components.
Each page is implemented as a module with a show_*_page() function.
"""

# The imports below make the page functions available when importing from pages
# This allows streamlit_app.py to use cleaner imports like: from pages import show_home_page

# Import all page display functions to make them available when importing from the pages package
from pages.home import show_home_page
from pages.management import show_resume_page
from pages.jobsearch import show_job_search_page
from pages.applicationdocuments import show_documents_page
from pages.applicationtracker import show_tracker_page
from pages.followupmanager import show_followup_page

# List all available pages for reference or programmatic access
__all__ = [
    'show_home_page',
    'show_resume_page',
    'show_job_search_page',
    'show_documents_page',
    'show_tracker_page',
    'show_followup_page'
]
