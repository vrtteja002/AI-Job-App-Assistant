import streamlit as st
import os
import sys
from datetime import datetime
import pandas as pd
from pages.home import show_home_page
from pages.jobsearch import show_job_search_page
from pages.management import show_resume_page
from pages.applicationdocuments import show_documents_page
from pages.applicationtracker import show_tracker_page
from pages.followupmanager import show_followup_page


# Add the project root to Python's path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Import application components
from core.app import JobApplicationAutomator
from config import init_directories

def setup_page_config():
    """Configure page settings"""
    st.set_page_config(
        page_title="AI Job Application Assistant",
        page_icon="💼",
        layout="wide",
        initial_sidebar_state="expanded"
    )

def initialize_session_state():
    """Initialize session state for storing data between reruns"""
    if 'initialized' not in st.session_state:
        # Create necessary directories
        dirs = init_directories()
        
        # Initialize the automator
        automator = JobApplicationAutomator()
        
        # Set initial session state values
        st.session_state.automator = automator
        st.session_state.dirs = dirs
        st.session_state.resume_loaded = False
        st.session_state.job_description = None
        st.session_state.job_analysis = None
        st.session_state.cover_letter = None
        st.session_state.search_results = None
        st.session_state.initialized = True

def show_sidebar():
    """Display sidebar navigation and API key input"""
    st.sidebar.title("AI Job Application Assistant")
    page = st.sidebar.radio(
        "Navigate",
        ["Home", "Resume Management", "Job Search", "Application Documents", "Application Tracker", "Follow-up Manager"]
    )
    
    # API key input in sidebar
    api_key = st.sidebar.text_input("OpenAI API Key", type="password", 
                                help="Enter your OpenAI API key to enable AI features")
    
    if api_key:
        os.environ["OPENAI_API_KEY"] = api_key
        # Reinitialize automator with the API key if provided
        st.session_state.automator = JobApplicationAutomator()
    
    # Footer
    st.sidebar.markdown("By Ravi Teja Vempati")
    
    return page

def add_custom_styles():
    """Add custom CSS styles to the app"""
    st.markdown("""
    <style>
        .stTabs [data-baseweb="tab-list"] {
            gap: 24px;
        }
        
        .stTabs [data-baseweb="tab"] {
            height: 50px;
            white-space: pre-wrap;
            border-radius: 4px 4px 0 0;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: rgba(128, 128, 128, 0.1);
        }
        
        div.stButton > button:first-child {
            width: 100%;
        }
    </style>
    """, unsafe_allow_html=True)

def run_streamlit_app():
    """Run the Streamlit application"""
    # Setup page configuration
    setup_page_config()
    
    # Initialize session state
    initialize_session_state()
    
    # Display sidebar and get selected page
    page = show_sidebar()
    
    # Display selected page
    if page == "Home":
        show_home_page()
    elif page == "Resume Management":
        show_resume_page()
    elif page == "Job Search":
        show_job_search_page()
    elif page == "Application Documents":
        show_documents_page()
    elif page == "Application Tracker":
        show_tracker_page()
    elif page == "Follow-up Manager":
        show_followup_page()
    
    # Add custom styling
    add_custom_styles()

if __name__ == "__main__":
    run_streamlit_app()
