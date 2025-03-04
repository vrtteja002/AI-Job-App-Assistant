from core.jobsearch import GoogleJobsSearch, SimulatedJobSearch

class JobSearchFactory:
    """
    Factory class for creating job search instances
    """
    
    @staticmethod
    def create_job_search(search_type="google", **kwargs):
        """
        Create a job search instance based on the specified type
        
        Args:
            search_type (str): Type of job search ("google", "simulated")
            **kwargs: Additional arguments to pass to the job search constructor
            
        Returns:
            JobSearchAPI: A job search instance
        """
        search_type = search_type.lower()
        
        if search_type == "google":
            return GoogleJobsSearch(**kwargs)
        elif search_type == "simulated":
            return SimulatedJobSearch(**kwargs)
        else:
            # Default to Google Jobs search
            print(f"Unknown search type: {search_type}. Using Google Jobs search.")
            return GoogleJobsSearch(**kwargs)
