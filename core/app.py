import os
from dotenv import load_dotenv
from core.resumeprocessor import ResumeProcessor
from core.jobanalyzer import JobAnalyzer
from core.documentgenerator import DocumentGenerator
from core.applicationtracker import ApplicationTracker
from core.jobsearchfactory import JobSearchFactory

# Load environment variables from .env file
load_dotenv()
import os
from dotenv import load_dotenv
from core.resumeprocessor import ResumeProcessor
from core.jobanalyzer import JobAnalyzer
from core.documentgenerator import DocumentGenerator
from core.applicationtracker import ApplicationTracker
from core.jobsearchfactory import JobSearchFactory

# Load environment variables from .env file
load_dotenv()

class JobApplicationAutomator:
    def __init__(self):
        # Initialize API key from environment variables
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            print("Warning: No OpenAI API key found. API features will be disabled.")
        
        # Initialize components
        self.resume_processor = ResumeProcessor(self.api_key)
        self.job_analyzer = JobAnalyzer(self.api_key)
        self.document_generator = DocumentGenerator(self.api_key)
        self.application_tracker = ApplicationTracker()
        
        # Initialize job search engine (defaults to Google Jobs)
        self.job_search_type = os.getenv("JOB_SEARCH_TYPE", "google")
        self.job_search = JobSearchFactory.create_job_search(self.job_search_type)
        
    def load_resume(self, resume_path):
        """Load and process the user's resume"""
        self.resume_processor.load_resume(resume_path)
        return self.resume_processor.get_resume_highlights()
        
    def analyze_job_description(self, job_description):
        """Analyze a job description to extract key requirements"""
        return self.job_analyzer.analyze_job_description(job_description)
    
    def generate_tailored_resume(self, job_description, output_path):
        """Generate a tailored resume based on job description"""
        resume_highlights = self.resume_processor.get_resume_highlights()
        job_analysis = self.job_analyzer.analyze_job_description(job_description)
        
        return self.document_generator.generate_tailored_resume(
            resume_highlights, 
            job_analysis, 
            output_path
        )
    
    def generate_cover_letter(self, company_name, position, job_description):
        """Generate a customized cover letter"""
        resume_highlights = self.resume_processor.get_resume_highlights()
        job_analysis = self.job_analyzer.analyze_job_description(job_description)
        
        return self.document_generator.generate_cover_letter(
            company_name,
            position,
            resume_highlights,
            job_analysis
        )
    
    def search_jobs(self, query, location=None, limit=10):
        """
        Search for jobs using the configured job search engine
        
        Args:
            query (str): Job search query
            location (str): Job location
            limit (int): Maximum number of results to return
            
        Returns:
            dict: Job search results
        """
        return self.job_search.search_jobs(query, location, limit)
    
    def track_application(self, company, position, status="Applied", notes=""):
        """Add an application to the tracking system"""
        self.application_tracker.track_application(company, position, status, notes)
        
    def generate_follow_up_email(self, company, position):
        """Generate a follow-up email for a specific application"""
        application = self.application_tracker.get_application(company, position)
        if application:
            return self.document_generator.generate_follow_up_email(company, position, application)
        return "No application found for this company and position."
    
    def suggest_applications(self, job_search_results):
        """Analyze multiple job postings and suggest which to apply for"""
        resume_highlights = self.resume_processor.get_resume_highlights()
        return self.job_analyzer.suggest_applications(resume_highlights, job_search_results)
    
    def save_application_tracker(self, file_path):
        """Save the application tracking data to a CSV file"""
        self.application_tracker.save_tracker(file_path)
        
    def load_application_tracker(self, file_path):
        """Load application tracking data from a CSV file"""
        self.application_tracker.load_tracker(file_path)
        
    def get_due_follow_ups(self):
        """Get applications due for follow-up"""
        return self.application_tracker.get_due_follow_ups()


# Example usage
if __name__ == "__main__":
    automator = JobApplicationAutomator()
    
    # Test functionality if run directly
    print("Job Application Automator initialized.")
    print("Use this module as part of the streamlit app or CLI.")
class JobApplicationAutomator:
    def __init__(self):
        # Initialize API key from environment variables
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            print("Warning: No OpenAI API key found. API features will be disabled.")
        
        # Initialize components
        self.resume_processor = ResumeProcessor(self.api_key)
        self.job_analyzer = JobAnalyzer(self.api_key)
        self.document_generator = DocumentGenerator(self.api_key)
        self.application_tracker = ApplicationTracker()
        
    def load_resume(self, resume_path):
        """Load and process the user's resume"""
        self.resume_processor.load_resume(resume_path)
        return self.resume_processor.get_resume_highlights()
        
    def analyze_job_description(self, job_description):
        """Analyze a job description to extract key requirements"""
        return self.job_analyzer.analyze_job_description(job_description)
    
    def generate_tailored_resume(self, job_description, output_path):
        """Generate a tailored resume based on job description"""
        resume_highlights = self.resume_processor.get_resume_highlights()
        job_analysis = self.job_analyzer.analyze_job_description(job_description)
        
        return self.document_generator.generate_tailored_resume(
            resume_highlights, 
            job_analysis, 
            output_path
        )
    
    def generate_cover_letter(self, company_name, position, job_description):
        """Generate a customized cover letter"""
        resume_highlights = self.resume_processor.get_resume_highlights()
        job_analysis = self.job_analyzer.analyze_job_description(job_description)
        
        return self.document_generator.generate_cover_letter(
            company_name,
            position,
            resume_highlights,
            job_analysis
        )
    
    def track_application(self, company, position, status="Applied", notes=""):
        """Add an application to the tracking system"""
        self.application_tracker.track_application(company, position, status, notes)
        
    def generate_follow_up_email(self, company, position):
        """Generate a follow-up email for a specific application"""
        application = self.application_tracker.get_application(company, position)
        if application:
            return self.document_generator.generate_follow_up_email(company, position, application)
        return "No application found for this company and position."
    
    def suggest_applications(self, job_search_results):
        """Analyze multiple job postings and suggest which to apply for"""
        resume_highlights = self.resume_processor.get_resume_highlights()
        return self.job_analyzer.suggest_applications(resume_highlights, job_search_results)
    
    def save_application_tracker(self, file_path):
        """Save the application tracking data to a CSV file"""
        self.application_tracker.save_tracker(file_path)
        
    def load_application_tracker(self, file_path):
        """Load application tracking data from a CSV file"""
        self.application_tracker.load_tracker(file_path)
        
    def get_due_follow_ups(self):
        """Get applications due for follow-up"""
        return self.application_tracker.get_due_follow_ups()


# Example usage
if __name__ == "__main__":
    automator = JobApplicationAutomator()
    
    # Test functionality if run directly
    print("Job Application Automator initialized.")
    print("Use this module as part of the streamlit app or CLI.")
