import os
import sys

# Add the current directory to Python's path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import Streamlit runner
from stream.app import run_streamlit_app

if __name__ == "__main__":
    run_streamlit_app()
