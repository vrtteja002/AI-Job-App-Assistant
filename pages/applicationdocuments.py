import streamlit as st
import os
import json
import tempfile
from datetime import datetime

from utils.helpers import ensure_directory_exists, save_text_to_file

def show_documents_page():
    """Display the application documents page"""
    st.title("📝 Application Documents")
    
    # Check if resume is loaded
    if not st.session_state.resume_loaded:
        st.warning("Please upload your resume first in the Resume Management section.")
    else:
        tabs = st.tabs(["Job Analysis", "Cover Letter", "Tailored Resume"])
        
        # Job Analysis tab
        with tabs[0]:
            st.subheader("Job Description Analysis")
            
            # Option to paste job description
            job_description = st.text_area("Paste Job Description", 
                                         value=st.session_state.get('job_description', ''),
                                         height=300)
            
            col1, col2 = st.columns([1, 1])
            
            with col1:
                company_name = st.text_input("Company Name")
            
            with col2:
                position_title = st.text_input("Position Title")
            
            if st.button("Analyze Job Description"):
                api_key = os.getenv("OPENAI_API_KEY")
                if not api_key:
                    st.error("Please enter your OpenAI API key in the sidebar first.")
                elif not job_description:
                    st.error("Please enter a job description to analyze.")
                else:
                    with st.spinner("Analyzing job description..."):
                        st.session_state.job_description = job_description
                        st.session_state.job_analysis = st.session_state.automator.analyze_job_description(job_description)
                        
                        # Store company and position if provided
                        if company_name:
                            st.session_state.company_name = company_name
                        if position_title:
                            st.session_state.position_title = position_title
            
            # Display job analysis
            if 'job_analysis' in st.session_state and st.session_state.job_analysis:
                st.subheader("Analysis Results")
                try:
                    # Try to parse as JSON
                    analysis_json = json.loads(st.session_state.job_analysis)
                    st.json(analysis_json)
                except:
                    # If not JSON, display as text
                    st.text_area("Analysis", st.session_state.job_analysis, height=300)
        
        # Cover Letter tab
        with tabs[1]:
            st.subheader("Generate Cover Letter")
            
            if not st.session_state.get('job_description') or not st.session_state.get('job_analysis'):
                st.warning("Please analyze a job description first.")
            else:
                # Pre-fill from session state if available
                default_company = st.session_state.get('company_name', '')
                default_position = st.session_state.get('position_title', '')
                
                col1, col2 = st.columns(2)
                with col1:
                    company_name = st.text_input("Company Name", value=default_company, key="cl_company")
                with col2:
                    position_title = st.text_input("Position Title", value=default_position, key="cl_position")
                
                if not company_name or not position_title:
                    st.warning("Please enter company name and position title.")
                elif st.button("Generate Cover Letter"):
                    api_key = os.getenv("OPENAI_API_KEY")
                    if not api_key:
                        st.error("Please enter your OpenAI API key in the sidebar first.")
                    else:
                        with st.spinner("Generating cover letter..."):
                            st.session_state.cover_letter = st.session_state.automator.generate_cover_letter(
                                company_name,
                                position_title,
                                st.session_state.job_description
                            )
                            
                            # Update session state
                            st.session_state.company_name = company_name
                            st.session_state.position_title = position_title
            
            # Display cover letter
            if st.session_state.get('cover_letter'):
                st.subheader("Your Cover Letter")
                st.text_area("Cover Letter", st.session_state.cover_letter, height=400)
                
                # Provide download link
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                company_safe = company_name.replace(' ', '_').lower()
                position_safe = position_title.replace(' ', '_').lower()
                filename = f"cover_letter_{company_safe}_{position_safe}_{timestamp}.txt"
                
                # Save for download
                output_path = os.path.join("outputs", filename)
                ensure_directory_exists(os.path.dirname(output_path))
                save_text_to_file(st.session_state.cover_letter, output_path)
                
                with open(output_path, "r") as f:
                    st.download_button(
                        label="Download Cover Letter",
                        data=f,
                        file_name=filename,
                        mime="text/plain"
                    )
                
                # Option to track application
                if st.button("Track This Application"):
                    try:
                        # Load tracker
                        st.session_state.automator.load_application_tracker("data/application_tracker.csv")
                    except:
                        pass
                        
                    # Track application
                    st.session_state.automator.track_application(company_name, position_title)
                    
                    # Save tracker
                    st.session_state.automator.save_application_tracker("data/application_tracker.csv")
                    st.success(f"Application for {position_title} at {company_name} tracked successfully.")
        
        # Tailored Resume tab
        with tabs[2]:
            st.subheader("Generate Tailored Resume")
            
            if not st.session_state.get('job_description') or not st.session_state.get('job_analysis'):
                st.warning("Please analyze a job description first.")
            else:
                if st.button("Generate Tailored Resume Guidance"):
                    api_key = os.getenv("OPENAI_API_KEY")
                    if not api_key:
                        st.error("Please enter your OpenAI API key in the sidebar first.")
                    else:
                        with st.spinner("Generating tailored resume guidance..."):
                            # Generate temp output file
                            with tempfile.NamedTemporaryFile(delete=False, suffix=".txt") as tmp_file:
                                output_path = tmp_file.name
                            
                            tailored_resume = st.session_state.automator.generate_tailored_resume(
                                st.session_state.job_description,
                                output_path
                            )
                            
                            # Store in session state
                            st.session_state.tailored_resume = tailored_resume
                            
                            # Display the guidance
                            st.subheader("Tailored Resume Guidance")
                            st.text_area("Guidance", tailored_resume, height=400)
                            
                            # Provide download link
                            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                            filename = f"resume_guidance_{timestamp}.txt"
                            
                            # Save for download
                            output_path = os.path.join("outputs", filename)
                            ensure_directory_exists(os.path.dirname(output_path))
                            save_text_to_file(tailored_resume, output_path)
                            
                            with open(output_path, "r") as f:
                                st.download_button(
                                    label="Download Resume Guidance",
                                    data=f,
                                    file_name=filename,
                                    mime="text/plain"
                                )
