import requests
import json
import os
from datetime import datetime
from bs4 import BeautifulSoup
import re
from utils.helpers import ensure_directory_exists, save_text_to_file

class JobSearchAPI:
    """Base class for job search API integrations"""
    
    def __init__(self, api_key=None):
        self.api_key = api_key
        self.data_dir = ensure_directory_exists(os.path.join("data", "job_listings"))
    
    def search_jobs(self, query, location=None, limit=10):
        """
        Search for jobs - to be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement search_jobs")
    
    def save_search_results(self, results, filename=None):
        """
        Save search results to a file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"job_search_{timestamp}.json"
            
        file_path = os.path.join(self.data_dir, filename)
        save_text_to_file(json.dumps(results, indent=2), file_path)
        
        return file_path


class GoogleJobsSearch(JobSearchAPI):
    """
    Class for searching and extracting job listings from Google Jobs
    """
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://www.google.com/search"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
    
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
                
                # Generate requirements based on job title and description
                requirements = self._generate_requirements_from_description(title, description)
                
                # Create job posting object
                job_posting = {
                    "title": title,
                    "company": company,
                    "location": location,
                    "description": description,
                    "requirements": requirements,
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
    
    def _generate_requirements_from_description(self, title, description):
        """
        Extract or generate requirements based on job title and description
        
        Args:
            title (str): Job title
            description (str): Job description
            
        Returns:
            list: List of requirements
        """
        # Base requirements that are common for most jobs
        base_requirements = [
            "Bachelor's degree in a relevant field",
            "Strong communication and teamwork skills",
            "Problem-solving abilities"
        ]
        
        # Extract potential requirements from description
        skill_keywords = [
            "experience with", "knowledge of", "proficiency in", "expertise in",
            "familiarity with", "skills in", "background in", "degree in",
            "certification in", "qualified in", "trained in"
        ]
        
        # Extract specific skills mentioned in the description
        extracted_reqs = []
        for keyword in skill_keywords:
            matches = re.finditer(f"{keyword}\\s+([^.;]*)[.;]", description.lower())
            for match in matches:
                if match.group(1).strip():
                    req = f"{keyword.capitalize()} {match.group(1).strip()}"
                    extracted_reqs.append(req)
        
        # Combine base and extracted requirements
        all_requirements = base_requirements + extracted_reqs
        
        # Add job-specific requirements based on title
        title_lower = title.lower()
        if "software" in title_lower or "developer" in title_lower:
            all_requirements.append("Experience with software development methodologies")
        elif "data" in title_lower:
            all_requirements.append("Experience with data analysis and visualization tools")
        elif "manager" in title_lower or "lead" in title_lower:
            all_requirements.append("Leadership and project management experience")
        
        # Return unique requirements (remove duplicates)
        return list(set(all_requirements))
    
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


class SimulatedJobSearch(JobSearchAPI):
    """
    Simulated job search for testing when online APIs are unavailable
    """
    
    def __init__(self):
        super().__init__()
    
    def search_jobs(self, query, location=None, limit=10):
        """
        Return simulated job search results
        """
        job_titles = [
            "Software Engineer", "Data Scientist", "Frontend Developer",
            "Backend Developer", "DevOps Engineer", "Product Manager",
            "UX Designer", "Machine Learning Engineer", "Full Stack Developer",
            "QA Engineer", "Systems Architect", "Database Administrator"
        ]
        
        companies = [
            "Tech Innovators Inc.", "DataCrunch Solutions", "WebFront Systems",
            "Cloud Nine Computing", "Agile Dynamics", "Product Visionaries",
            "UX Masters", "AI Learning Corp", "Full Range Technologies",
            "Quality Assurance Experts", "System Design Partners", "Data Storage Pro"
        ]
        
        results = []
        for i in range(min(limit, 10)):
            job_index = i % len(job_titles)
            company_index = i % len(companies)
            
            # Create job title that includes the search query if possible
            title = job_titles[job_index]
            if query.lower() not in title.lower():
                title = f"{title} - {query.capitalize()}"
            
            # Create job posting with more detailed information
            job_posting = {
                "title": title,
                "company": companies[company_index],
                "location": location or "Remote",
                "description": self._generate_job_description(title, query),
                "requirements": self._generate_requirements(title, query),
                "salary_range": "$90,000 - $140,000",
                "posted_date": (datetime.now().replace(
                    day=max(1, datetime.now().day - (i % 10))
                )).strftime("%Y-%m-%d"),
                "application_url": f"https://example.com/jobs/{i+1}",
                "job_id": f"JOB{i+1000}",
                "source": "Simulated"
            }
            
            results.append(job_posting)
            
        return {"results": results}
    
    def _generate_job_description(self, job_title, query):
        """Generate a realistic job description based on the title and query"""
        descriptions = {
            "Software Engineer": "We are looking for a Software Engineer to join our development team. You will be responsible for designing, coding, and modifying applications according to client specifications. As a member of our team, you will develop high-quality software design and architecture.",
            "Data Scientist": "We're seeking a Data Scientist to interpret data and turn it into information which can offer ways to improve our business. You'll be mining complex data and using advanced analytics to find patterns and relationships in data, then presenting these insights to stakeholders.",
            "Frontend Developer": "We need a Frontend Developer who will implement visual elements that users see and interact with in a web application. You'll collaborate with UI/UX designers and bridge the gap between graphical design and technical implementation.",
            "Backend Developer": "Join our team as a Backend Developer to build and maintain the server-side logic that powers our applications. You will develop all server-side logic, maintain databases, and ensure high performance and responsiveness to requests from the front-end.",
            "DevOps Engineer": "We're looking for a DevOps Engineer to help us build and scale our infrastructure. You will be responsible for designing, implementing, and maintaining our CI/CD pipelines as well as managing our cloud infrastructure."
        }
        
        base_desc = descriptions.get(job_title.split(" - ")[0], 
                                   f"We are hiring a talented {job_title} to join our team. In this role, you will work on challenging projects and collaborate with cross-functional teams to deliver high-quality solutions.")
        
        # Add query-specific information
        specific_desc = f"\n\nIn this role, you will focus specifically on {query.lower()} technologies and solutions. You will be working with cutting-edge tools and frameworks in the {query.lower()} space to develop innovative solutions for our clients."
        
        return base_desc + specific_desc
    
    def _generate_requirements(self, job_title, query):
        """Generate realistic requirements based on the job title and query"""
        base_requirements = [
            "Bachelor's degree in Computer Science or related field",
            "Excellent problem-solving skills",
            "Strong communication and teamwork abilities"
        ]
        
        specific_requirements = {
            "Software Engineer": [
                "3+ years of software development experience",
                f"Proficiency in {query}-related technologies",
                "Experience with software design patterns",
                "Knowledge of databases and data structures"
            ],
            "Data Scientist": [
                "Experience with data analysis tools like Python, R, or SAS",
                "Knowledge of machine learning frameworks",
                "Strong statistical and mathematical background",
                f"Experience with {query} data processing"
            ],
            "Frontend Developer": [
                "Expertise in JavaScript, HTML, and CSS",
                "Experience with React, Angular, or Vue",
                "Understanding of responsive design principles",
                f"Knowledge of {query} frameworks and libraries"
            ]
        }
        
        job_base = job_title.split(" - ")[0]
        requirements = base_requirements + specific_requirements.get(job_base, [
            f"Experience in {job_base} role",
            f"Technical knowledge of {query}",
            "Ability to learn quickly and adapt to new technologies"
        ])
        
        # Add a query-specific requirement
        requirements.append(f"Familiarity with {query.capitalize()} ecosystem and best practices")
        
        return requirements