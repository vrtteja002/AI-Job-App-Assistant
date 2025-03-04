import requests
import json
import os
from datetime import datetime
from bs4 import BeautifulSoup
import re
from utils.helpers import ensure_directory_exists, save_text_to_file

class GoogleJobsSearch:
    """
    Class for searching and extracting job listings from Google Jobs
    """
    
    def __init__(self):
        self.base_url = "https://www.google.com/search"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.data_dir = ensure_directory_exists(os.path.join("data", "job_listings"))
    
    def search_jobs(self, query, location=None, limit=10):
        """
        Search for jobs on Google Jobs
        
        Args:
            query (str): Job search query
            location (str): Job location
            limit (int): Maximum number of results to return
            
        Returns:
            dict: Job search results
        """
        # Format the search query for Google Jobs
        search_query = f"{query} jobs"
        if location:
            search_query += f" in {location}"
        
        # Parameters for the Google search
        params = {
            "q": search_query,
            "ibp": "htl;jobs",  # This parameter tells Google to show jobs
            "uule": "w+CAIQICI",  # Location encoding (can be adjusted for specific locations)
            "hl": "en",  # Language
            "gl": "us"   # Country
        }
        
        try:
            # Make the request to Google
            response = requests.get(self.base_url, params=params, headers=self.headers)
            response.raise_for_status()
            
            # Parse the HTML response
            return self._parse_job_listings(response.text, limit)
            
        except requests.RequestException as e:
            print(f"Error fetching job listings: {e}")
            return {"results": [], "error": str(e)}
    
    def _parse_job_listings(self, html_content, limit=10):
        """
        Parse job listings from HTML content
        
        Args:
            html_content (str): HTML content of the search results page
            limit (int): Maximum number of results to return
            
        Returns:
            dict: Parsed job listings
        """
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Find all job cards
        job_cards = soup.select('div.iFjolb')
        
        results = []
        for i, card in enumerate(job_cards[:limit]):
            if i >= limit:
                break
                
            try:
                # Extract job title
                title_elem = card.select_one('div.BjJfJf')
                title = title_elem.text.strip() if title_elem else "Unknown Title"
                
                # Extract company name
                company_elem = card.select_one('div.vNEEBe')
                company = company_elem.text.strip() if company_elem else "Unknown Company"
                
                # Extract location
                location_elem = card.select_one('div.Qk80Jf')
                location = location_elem.text.strip() if location_elem else "Remote"
                
                # Extract description snippet
                description_elem = card.select_one('div.HBvzbc')
                description = description_elem.text.strip() if description_elem else ""
                
                # Extract posting date
                date_elem = card.select_one('div.KKh3md span.LL4CDc')
                posted_date = date_elem.text.strip() if date_elem else "Recently"
                
                # Create job posting object
                job_posting = {
                    "title": title,
                    "company": company,
                    "location": location,
                    "description": description,
                    "posted_date": posted_date,
                    "source": "Google Jobs",
                    "job_id": f"GJ{i+1000}"
                }
                
                # Additional details (might need to be fetched separately)
                link_elem = card.select_one('a.pMhGee')
                if link_elem and 'href' in link_elem.attrs:
                    job_posting["application_url"] = "https://www.google.com" + link_elem['href']
                
                results.append(job_posting)
                
            except Exception as e:
                print(f"Error parsing job card: {e}")
                continue
        
        return {"results": results}
    
    def get_job_details(self, job_url):
        """
        Get detailed information for a specific job listing
        
        Args:
            job_url (str): URL of the job listing
            
        Returns:
            dict: Detailed job information
        """
        try:
            response = requests.get(job_url, headers=self.headers)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract detailed job information
            job_details = {}
            
            # Extract full description
            description_elem = soup.select_one('div.job-description')
            if description_elem:
                job_details["full_description"] = description_elem.text.strip()
            
            # Extract requirements
            requirements_elem = soup.select_one('div.requirements')
            if requirements_elem:
                requirements_text = requirements_elem.text.strip()
                # Split by bullet points or newlines
                requirements = [req.strip() for req in re.split(r'•|\n', requirements_text) if req.strip()]
                job_details["requirements"] = requirements
            
            # Extract salary information
            salary_elem = soup.select_one('div.salary-range')
            if salary_elem:
                job_details["salary_range"] = salary_elem.text.strip()
            
            return job_details
            
        except requests.RequestException as e:
            print(f"Error fetching job details: {e}")
            return {}
    
    def save_search_results(self, results, filename=None):
        """
        Save search results to a file
        
        Args:
            results (dict): Job search results
            filename (str, optional): Name of the file to save results to
            
        Returns:
            str: Path to the saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"job_search_{timestamp}.json"
            
        file_path = os.path.join(self.data_dir, filename)
        save_text_to_file(json.dumps(results, indent=2), file_path)
        
        return file_path
