import pandas as pd
import os
from datetime import datetime, timedelta

class ApplicationTracker:
    def __init__(self):
        self.tracker = pd.DataFrame(columns=[
            'company', 'position', 'date_applied', 'status', 'follow_up_date', 
            'last_contact_date', 'contact_person', 'contact_email', 'notes'
        ])
    
    def track_application(self, company, position, status="Applied", notes=""):
        """Add a new application to the tracker"""
        today = datetime.now().strftime("%Y-%m-%d")
        follow_up = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        
        new_application = pd.DataFrame({
            'company': [company],
            'position': [position],
            'date_applied': [today],
            'status': [status],
            'follow_up_date': [follow_up],
            'last_contact_date': [today],
            'contact_person': [""],
            'contact_email': [""],
            'notes': [notes]
        })
        
        # Check if this application already exists
        existing = self.tracker[
            (self.tracker['company'] == company) & 
            (self.tracker['position'] == position)
        ]
        
        if len(existing) > 0:
            # Update existing application
            self.update_application(company, position, status=status, notes=notes)
        else:
            # Add new application
            self.tracker = pd.concat([self.tracker, new_application], ignore_index=True)
            print(f"Application for {position} at {company} has been tracked.")
    
    def update_application(self, company, position, status=None, 
                          follow_up_date=None, last_contact_date=None,
                          contact_person=None, contact_email=None, notes=None):
        """Update an existing application"""
        # Find the application
        mask = (self.tracker['company'] == company) & (self.tracker['position'] == position)
        
        if not any(mask):
            print(f"No application found for {position} at {company}")
            return False
        
        # Update the fields that were provided
        if status:
            self.tracker.loc[mask, 'status'] = status
            
        if follow_up_date:
            self.tracker.loc[mask, 'follow_up_date'] = follow_up_date
            
        if last_contact_date:
            self.tracker.loc[mask, 'last_contact_date'] = last_contact_date
        
        if contact_person:
            self.tracker.loc[mask, 'contact_person'] = contact_person
            
        if contact_email:
            self.tracker.loc[mask, 'contact_email'] = contact_email
            
        if notes:
            # Append to existing notes
            existing_notes = self.tracker.loc[mask, 'notes'].iloc[0]
            updated_notes = existing_notes
            if existing_notes:
                today = datetime.now().strftime("%Y-%m-%d")
                updated_notes = f"{existing_notes}\n\n{today}: {notes}"
            else:
                updated_notes = notes
                
            self.tracker.loc[mask, 'notes'] = updated_notes
        
        print(f"Application for {position} at {company} has been updated.")
        return True
    
    def get_application(self, company, position):
        """Get a specific application"""
        application = self.tracker[
            (self.tracker['company'] == company) & 
            (self.tracker['position'] == position)
        ]
        
        if application.empty:
            return None
        
        # Convert to dictionary
        return application.iloc[0].to_dict()
    
    def get_all_applications(self, status=None):
        """Get all applications, optionally filtered by status"""
        if status:
            return self.tracker[self.tracker['status'] == status]
        return self.tracker
    
    def get_due_follow_ups(self):
        """Get applications due for follow-up"""
        today = datetime.now().strftime("%Y-%m-%d")
        follow_ups = self.tracker[
            (self.tracker['follow_up_date'] <= today) & 
            (self.tracker['status'] == "Applied")
        ]
        
        return follow_ups
    
    def save_tracker(self, file_path):
        """Save tracker to CSV file"""
        # Ensure the directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        self.tracker.to_csv(file_path, index=False)
        print(f"Application tracking data saved to {file_path}")
    
    def load_tracker(self, file_path):
        """Load tracker from CSV file"""
        try:
            self.tracker = pd.read_csv(file_path)
            print(f"Application tracking data loaded from {file_path}")
        except Exception as e:
            print(f"Error loading tracker: {e}")
    
    def get_application_statistics(self):
        """Get statistics about applications"""
        stats = {
            'total_applications': len(self.tracker),
            'status_counts': self.tracker['status'].value_counts().to_dict(),
            'companies_applied': self.tracker['company'].nunique(),
            'positions_applied': self.tracker['position'].nunique(),
            'oldest_application': self.tracker['date_applied'].min() if not self.tracker.empty else None,
            'newest_application': self.tracker['date_applied'].max() if not self.tracker.empty else None,
        }
        
        return stats
    
    def delete_application(self, company, position):
        """Delete an application from the tracker"""
        before_count = len(self.tracker)
        self.tracker = self.tracker[
            ~((self.tracker['company'] == company) & (self.tracker['position'] == position))
        ]
        
        if len(self.tracker) < before_count:
            print(f"Application for {position} at {company} has been deleted.")
            return True
        else:
            print(f"No application found for {position} at {company}")
            return False
