import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# LLM Settings
DEFAULT_TEMPERATURE = 0.7
RESUME_ANALYSIS_TEMPERATURE = 0.2
JOB_ANALYSIS_TEMPERATURE = 0.3
COVER_LETTER_TEMPERATURE = 0.7

# Application Settings
DEFAULT_FOLLOW_UP_DAYS = 14
OUTPUT_DIRECTORY = "outputs"
DATA_DIRECTORY = "data"
RESUME_FILE = os.path.join(DATA_DIRECTORY, "resume.pdf")
TRACKER_FILE = os.path.join(DATA_DIRECTORY, "application_tracker.csv")

# Document Templates
RESUME_TEMPLATE = os.path.join(DATA_DIRECTORY, "templates", "resume_template.md")
COVER_LETTER_TEMPLATE = os.path.join(DATA_DIRECTORY, "templates", "cover_letter_template.md")
EMAIL_TEMPLATE = os.path.join(DATA_DIRECTORY, "templates", "email_template.md")

# Application Statuses
APP_STATUS = {
    "APPLIED": "Applied",
    "INTERVIEW": "Interview Scheduled",
    "FOLLOW_UP": "Follow-up Sent",
    "REJECTED": "Rejected",
    "OFFER": "Offer Received",
    "ACCEPTED": "Offer Accepted",
    "WITHDRAWN": "Withdrawn"
}

# Email Settings
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", "587"))
EMAIL_USERNAME = os.getenv("EMAIL_USERNAME", "")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD", "")
EMAIL_FROM = os.getenv("EMAIL_FROM", "")

# Initialize required directories
def init_directories():
    """Create required directories if they don't exist."""
    os.makedirs(OUTPUT_DIRECTORY, exist_ok=True)
    os.makedirs(DATA_DIRECTORY, exist_ok=True)
    os.makedirs(os.path.join(DATA_DIRECTORY, "templates"), exist_ok=True)
    os.makedirs(os.path.join(DATA_DIRECTORY, "job_listings"), exist_ok=True)
    
    return {
        "output_dir": OUTPUT_DIRECTORY,
        "data_dir": DATA_DIRECTORY,
        "templates_dir": os.path.join(DATA_DIRECTORY, "templates"),
        "job_listings_dir": os.path.join(DATA_DIRECTORY, "job_listings")
    }
