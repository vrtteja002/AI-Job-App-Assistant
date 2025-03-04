from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

class JobAnalyzer:
    def __init__(self, api_key):
        self.api_key = api_key
        
        # Initialize LLM if API key is available
        if self.api_key:
            self.llm = ChatOpenAI(openai_api_key=api_key, temperature=0.7,model="gpt-4o")
        else:
            self.llm = None
    
    def analyze_job_description(self, job_description):
        """Analyze a job description to extract key requirements"""
        if not self.api_key:
            return "API key required for job description analysis."
            
        prompt = PromptTemplate(
            input_variables=["job_description"],
            template="""
            Analyze the following job description and extract:
            1. Required technical skills (list all mentioned)
            2. Required soft skills
            3. Experience level required (years and seniority)
            4. Key responsibilities (top 5)
            5. Company values mentioned
            
            Job Description:
            {job_description}
            
            Format your response like :
            Required technical skills (list all mentioned):
            2. Required soft skills:
            3. Experience level required (years and seniority):
            4. Key responsibilities (top 5):
            5. Company values mentioned:.
            """
        )
        
        job_analysis_chain = LLMChain(llm=self.llm, prompt=prompt)
        job_analysis = job_analysis_chain.run(job_description=job_description)
        
        return job_analysis
    
    def suggest_applications(self, resume_highlights, job_listings):
        """Analyze multiple job postings and suggest which to apply for"""
        if not self.api_key:
            return "API key required for job suggestion analysis."
            
        if not resume_highlights:
            return "No resume highlights available. Please load your resume first."
        
        prompt = PromptTemplate(
            input_variables=["resume_highlights", "job_listings"],
            template="""
            Based on my background and the following job listings, rank the positions from most suitable to least suitable.
            
            My background:
            {resume_highlights}
            
            Job listings:
            {job_listings}
            
            For each position, provide:
            1. Compatibility score (1-10)
            2. Key matching qualifications
            3. Potential gaps to address
            4. Suggested approach for application
            
            Rank them in order of recommendation.
            """
        )
        
        suggestion_chain = LLMChain(llm=self.llm, prompt=prompt)
        suggestions = suggestion_chain.run(
            resume_highlights=resume_highlights,
            job_listings=job_listings
        )
        
        return suggestions
    
    def calculate_match_score(self, resume_highlights, job_description):
        """Calculate how well a candidate matches a job description"""
        if not self.api_key:
            return "API key required for match score calculation."
            
        job_analysis = self.analyze_job_description(job_description)
        
        prompt = PromptTemplate(
            input_variables=["resume_highlights", "job_analysis"],
            template="""
            Calculate a match score (0-100) between the candidate profile and job requirements.
            
            Candidate profile:
            {resume_highlights}
            
            Job requirements:
            {job_analysis}
            
            Provide:
            1. Overall match score (0-100)
            2. Score breakdown by category (skills, experience, education)
            3. Strongest matching points
            4. Areas for improvement
            5. Suggested talking points for interview
            
            Format your response as JSON.
            """
        )
        
        match_chain = LLMChain(llm=self.llm, prompt=prompt)
        match_analysis = match_chain.run(
            resume_highlights=resume_highlights,
            job_analysis=job_analysis
        )
        
        return match_analysis
