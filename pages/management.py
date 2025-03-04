import streamlit as st
import tempfile
import json
import os

def show_resume_page():
    """Display the resume management page"""
    st.title("📄 Resume Management")
    
    # Upload resume
    st.subheader("Upload Your Resume")
    uploaded_file = st.file_uploader("Choose a PDF or text file", type=["pdf", "txt"])
    
    if uploaded_file is not None:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{uploaded_file.name.split('.')[-1]}") as tmp_file:
            tmp_file.write(uploaded_file.getvalue())
            resume_path = tmp_file.name
        
        if st.button("Process Resume"):
            api_key = os.getenv("OPENAI_API_KEY")
            if not api_key:
                st.error("Please enter your OpenAI API key in the sidebar first.")
            else:
                with st.spinner("Processing resume..."):
                    try:
                        resume_highlights = st.session_state.automator.load_resume(resume_path)
                        st.session_state.resume_loaded = True
                        st.success("Resume processed successfully!")
                        
                        # Display resume highlights
                        st.subheader("Resume Highlights")
                        try:
                            # Try to parse as JSON
                            highlights_json = json.loads(resume_highlights)
                            st.json(highlights_json)
                        except:
                            # If not JSON, display as text
                            st.text_area("Extracted Information", resume_highlights, height=300)
                    except Exception as e:
                        st.error(f"Error processing resume: {str(e)}")
    
    # Display current resume status
    if st.session_state.resume_loaded:
        st.info("✅ Resume is loaded and ready for use")
        
        # Option to view resume text
        if st.button("View Full Resume Text"):
            try:
                resume_text = st.session_state.automator.resume_processor.get_resume_text()
                st.text_area("Resume Text", resume_text, height=400)
            except Exception as e:
                st.error(f"Error retrieving resume text: {str(e)}")
                
        # Tips for optimizing your resume
        with st.expander("Resume Optimization Tips"):
            st.markdown("""
            ### Tips for Optimizing Your Resume
            
            1. **Use Keywords from Job Descriptions**
               - Include relevant keywords that match the job descriptions
               - Our AI analysis will help identify skills to emphasize
            
            2. **Quantify Achievements**
               - Use numbers to demonstrate impact (e.g., "Increased efficiency by 25%")
               - Specific metrics make your experience more concrete
            
            3. **Customize for Each Application**
               - Use the "Application Documents" section to generate tailored resumes
               - Adjust emphasis based on each job's specific requirements
            
            4. **Keep Format ATS-Friendly**
               - Use standard headings (Education, Experience, Skills)
               - Avoid complex formatting, tables, or graphics
            
            5. **Focus on Relevant Experience**
               - Prioritize experience relevant to your target positions
               - Place most relevant information first
            """)
    else:
        st.warning("❌ No resume loaded. Please upload your resume.")
