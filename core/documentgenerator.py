from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from datetime import datetime, timedelta

class DocumentGenerator:
    def __init__(self, api_key):
        self.api_key = api_key
        
        # Initialize LLM if API key is available
        if self.api_key:
            self.llm = ChatOpenAI(openai_api_key=api_key, temperature=0.7,model="gpt-4o")
        else:
            self.llm = None
    
    def generate_tailored_resume(self, resume_highlights, job_analysis, output_path):
        """Generate a tailored resume based on job description"""
        if not self.api_key:
            message = "API key required for generating tailored resume guidance."
            with open(output_path, 'w') as f:
                f.write(message)
            return message
            
        prompt = PromptTemplate(
            input_variables=["resume_highlights", "job_analysis"],
            template="""
            Create a tailored resume based on my profile and the job requirements.
            
            My profile:
            {resume_highlights}
            
            Job requirements:
            {job_analysis}
            
            Provide guidance on which sections of my resume to highlight, 
            which achievements to emphasize, and any skills that should be 
            more prominently featured to align with this specific job.
            """
        )
        
        resume_tailor_chain = LLMChain(llm=self.llm, prompt=prompt)
        tailored_resume_guidance = resume_tailor_chain.run(
            resume_highlights=resume_highlights,
            job_analysis=job_analysis
        )
        
        # This would need to be expanded to actually modify a resume document
        with open(output_path, 'w') as f:
            f.write(tailored_resume_guidance)
            
        return tailored_resume_guidance
    
    def generate_cover_letter(self, company_name, position, resume_highlights, job_analysis):
        """Generate a customized cover letter"""
        if not self.api_key:
            return "API key required for generating cover letter."
            
        prompt = PromptTemplate(
            input_variables=["company", "position", "resume_highlights", "job_analysis"],
            template="""
            Write a compelling cover letter for a {position} position at {company}.
            
            My background:
            {resume_highlights}
            
            Job requirements:
            {job_analysis}
            
            The cover letter should:
            1. Be professional and engaging
            2. Highlight my most relevant skills and experiences
            3. Show enthusiasm for the company and role
            4. Demonstrate how I meet the key requirements
            5. Include a call to action
            
            Write the complete cover letter in a standard format with date, address block, salutation, 
            3-4 substantive paragraphs, closing, and signature line.
            """
        )
        
        cover_letter_chain = LLMChain(llm=self.llm, prompt=prompt)
        cover_letter = cover_letter_chain.run(
            company=company_name,
            position=position,
            resume_highlights=resume_highlights,
            job_analysis=job_analysis
        )
        
        return cover_letter
    
    def generate_follow_up_email(self, company, position, application_data):
        """Generate a follow-up email for a specific application"""
        if not self.api_key:
            return "API key required for generating follow-up email."
            
        if not application_data:
            return "No application found for this company and position."
        
        prompt = PromptTemplate(
            input_variables=["company", "position", "days_since"],
            template="""
            Write a polite and professional follow-up email regarding my application for the {position} position at {company}.
            It has been {days_since} days since I submitted my application.
            
            The email should:
            1. Reference my application submission
            2. Express continued interest in the position
            3. Briefly highlight why I'm a good fit
            4. Request information on the status of my application
            5. Thank the recipient for their time
            
            Write the complete email with subject line, greeting, body, and signature.
            """
        )
        
        date_applied = datetime.strptime(application_data['date_applied'], "%Y-%m-%d")
        days_since = (datetime.now() - date_applied).days
        
        follow_up_chain = LLMChain(llm=self.llm, prompt=prompt)
        follow_up_email = follow_up_chain.run(
            company=company,
            position=position,
            days_since=days_since
        )
        
        return follow_up_email
        
    def generate_thank_you_email(self, company, position, interviewer_name, interview_notes):
        """Generate a thank you email after an interview"""
        if not self.api_key:
            return "API key required for generating thank you email."
            
        prompt = PromptTemplate(
            input_variables=["company", "position", "interviewer_name", "interview_notes"],
            template="""
            Write a personalized thank you email to send after my interview for the {position} position at {company}.
            
            Interviewer: {interviewer_name}
            
            Interview notes:
            {interview_notes}
            
            The email should:
            1. Express appreciation for the opportunity to interview
            2. Reference specific topics discussed during the interview
            3. Reinforce my interest in the role
            4. Address any concerns or questions that arose during the interview
            5. Keep a professional but warm tone
            
            Write the complete email with subject line, greeting, body, and signature.
            """
        )
        
        thank_you_chain = LLMChain(llm=self.llm, prompt=prompt)
        thank_you_email = thank_you_chain.run(
            company=company,
            position=position,
            interviewer_name=interviewer_name,
            interview_notes=interview_notes
        )
        
        return thank_you_email
        
    def generate_LinkedIn_message(self, company, position, recipient_name, connection_context):
        """Generate a LinkedIn connection or follow-up message"""
        if not self.api_key:
            return "API key required for generating LinkedIn message."
            
        prompt = PromptTemplate(
            input_variables=["company", "position", "recipient_name", "connection_context"],
            template="""
            Write a concise and effective LinkedIn message to {recipient_name} regarding the {position} role at {company}.
            
            Context: {connection_context}
            
            The message should:
            1. Be brief (under 300 characters for initial connection request)
            2. Explain why I'm reaching out
            3. Show specific interest in their company/team
            4. Include a clear call to action
            5. Be professional but conversational
            
            Write the complete message ready to send on LinkedIn.
            """
        )
        
        linkedin_chain = LLMChain(llm=self.llm, prompt=prompt)
        linkedin_message = linkedin_chain.run(
            company=company,
            position=position,
            recipient_name=recipient_name,
            connection_context=connection_context
        )
        
        return linkedin_message
