"""
This module contains the core application logic for the AI Job Application Assistant.
"""

# Import core modules for easier access
from core.app import JobApplicationAutomator
from core.resumeprocessor import ResumeProcessor
from core.jobanalyzer import JobAnalyzer
from core.documentgenerator import DocumentGenerator
from core.applicationtracker import ApplicationTracker
from core.emailsender import EmailSender
from core.jobsearch import SimulatedJobSearch

__all__ = [
    'JobApplicationAutomator',
    'ResumeProcessor',
    'JobAnalyzer',
    'DocumentGenerator',
    'ApplicationTracker',
    'EmailSender',
    'SimulatedJobSearch'
]
