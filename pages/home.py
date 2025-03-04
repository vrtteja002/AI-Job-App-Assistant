import streamlit as st
import os
import pandas as pd

def show_home_page():
    """Display the home page with system overview and status"""
    st.title("🤖 AI Job Application Assistant")
    
    st.markdown("""
    Welcome to the AI Job Application Assistant! This tool helps you streamline your job application process using AI.
    
    ### Features:
    - **Resume Management**: Upload and analyze your resume
    - **Job Search**: Find relevant job opportunities
    - **Application Documents**: Generate tailored resumes and cover letters
    - **Application Tracker**: Keep track of your job applications
    - **Follow-up Manager**: Generate and manage follow-up emails
    
    ### Getting Started:
    1. Enter your OpenAI API key in the sidebar
    2. Upload your resume in the Resume Management section
    3. Start searching for jobs or analyzing job descriptions
    """)
    
    # System status
    st.subheader("System Status")
    col1, col2 = st.columns(2)
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    with col1:
        st.info(f"API Key: {'✅ Configured' if api_key else '❌ Not Configured'}")
        st.info(f"Resume: {'✅ Loaded' if st.session_state.resume_loaded else '❌ Not Loaded'}")
    
    with col2:
        if os.path.exists(os.path.join("data", "application_tracker.csv")):
            try:
                df = pd.read_csv(os.path.join("data", "application_tracker.csv"))
                st.info(f"Applications Tracked: {len(df)}")
                st.info(f"Applications Pending Follow-up: {len(df[df['status'] == 'Applied'])}")
            except:
                st.info("Applications Tracked: 0")
                st.info("Applications Pending Follow-up: 0")
        else:
            st.info("Applications Tracked: 0")
            st.info("Applications Pending Follow-up: 0")
            
    # Quick stats if there's tracked data
    if os.path.exists(os.path.join("data", "application_tracker.csv")):
        try:
            df = pd.read_csv(os.path.join("data", "application_tracker.csv"))
            if not df.empty:
                st.subheader("Application Summary")
                
                # Statistics
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Total Applications", len(df))
                with col2:
                    status_counts = df['status'].value_counts().to_dict()
                    interview_count = status_counts.get('Interview Scheduled', 0)
                    st.metric("Interviews", interview_count)
                with col3:
                    offer_count = status_counts.get('Offer Received', 0) + status_counts.get('Offer Accepted', 0)
                    st.metric("Offers", offer_count)
                
                # Status breakdown
                st.subheader("Application Status")
                status_df = pd.DataFrame(df['status'].value_counts()).reset_index()
                status_df.columns = ['Status', 'Count']
                
                # Simple bar chart for status
                st.bar_chart(data=status_df, x='Status', y='Count')
        except Exception as e:
            st.error(f"Error loading application data: {str(e)}")
