import streamlit as st
import os
import pandas as pd
from datetime import datetime

from utils.helpers import ensure_directory_exists, save_text_to_file

def show_followup_page():
    """Display the follow-up manager page"""
    st.title("📧 Follow-up Manager")
    
    # Check for due follow-ups
    try:
        st.session_state.automator.load_application_tracker("data/application_tracker.csv")
        due_followups = st.session_state.automator.get_due_follow_ups()
    except:
        # If file doesn't exist yet, create an empty tracker
        st.session_state.automator.application_tracker.save_tracker("data/application_tracker.csv")
        due_followups = pd.DataFrame()
    
    # Display due follow-ups
    if not due_followups.empty:
        st.subheader(f"Follow-ups Due ({len(due_followups)})")
        st.dataframe(due_followups[['company', 'position', 'date_applied', 'follow_up_date']])
        
        # Quick action buttons
        st.subheader("Quick Actions")
        for i, app in due_followups.iterrows():
            col1, col2 = st.columns([3, 1])
            
            with col1:
                st.write(f"**{app['position']}** at **{app['company']}** (Applied: {app['date_applied']})")
            
            with col2:
                if st.button("Generate Email", key=f"quick_email_{i}"):
                    st.session_state.selected_company = app['company']
                    st.session_state.selected_position = app['position']
                    st.rerun()
    
    # Generate follow-up form
    st.subheader("Generate Follow-up Email")
    
    col1, col2 = st.columns(2)
    
    # Pre-fill values if coming from application tracker
    company_default = st.session_state.get('selected_company', '')
    position_default = st.session_state.get('selected_position', '')
    
    with col1:
        company = st.text_input("Company Name", value=company_default)
    
    with col2:
        position = st.text_input("Position Title", value=position_default)
    
    if st.button("Generate Follow-up Email"):
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            st.error("Please enter your OpenAI API key in the sidebar first.")
        elif not company or not position:
            st.error("Please enter company name and position title.")
        else:
            with st.spinner("Generating follow-up email..."):
                follow_up = st.session_state.automator.generate_follow_up_email(company, position)
                
                if follow_up == "No application found for this company and position.":
                    st.error(follow_up)
                else:
                    st.session_state.follow_up_email = follow_up
                    st.session_state.follow_up_company = company
                    st.session_state.follow_up_position = position
    
    # Display follow-up email
    if 'follow_up_email' in st.session_state:
        st.subheader("Follow-up Email")
        st.text_area("Email Content", st.session_state.follow_up_email, height=300)
        
        # Provide download link
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        company_safe = st.session_state.follow_up_company.replace(' ', '_').lower()
        position_safe = st.session_state.follow_up_position.replace(' ', '_').lower()
        filename = f"follow_up_{company_safe}_{position_safe}_{timestamp}.txt"
        
        # Save for download
        output_path = os.path.join("outputs", filename)
        ensure_directory_exists(os.path.dirname(output_path))
        save_text_to_file(st.session_state.follow_up_email, output_path)
        
        with open(output_path, "r") as f:
            st.download_button(
                label="Download Follow-up Email",
                data=f,
                file_name=filename,
                mime="text/plain"
            )
        
        # Option to update application status
        if st.button("Mark as Followed Up"):
            st.session_state.automator.application_tracker.update_application(
                st.session_state.follow_up_company, 
                st.session_state.follow_up_position, 
                status="Follow-up Sent",
                last_contact_date=datetime.now().strftime("%Y-%m-%d"),
                notes=f"Follow-up email sent on {datetime.now().strftime('%Y-%m-%d')}"
            )
            st.session_state.automator.save_application_tracker("data/application_tracker.csv")
            st.success("Application status updated to 'Follow-up Sent'")
            
            # Clear the form
            if 'selected_company' in st.session_state:
                del st.session_state.selected_company
            if 'selected_position' in st.session_state:
                del st.session_state.selected_position
            st.rerun()
    
    # Follow-up tips
    with st.expander("Follow-up Tips"):
        st.markdown("""
        ### Effective Follow-up Strategies
        
        1. **Timing is Key**
           - Send follow-ups 1-2 weeks after applying
           - Follow up within 24-48 hours after an interview
        
        2. **Maintain Professionalism**
           - Keep emails concise and to the point
           - Express continued interest in the position
           - Reference specific points from your application or interview
        
        3. **Provide Additional Value**
           - Include new accomplishments if relevant
           - Share relevant work samples or portfolio items
           - Mention recent industry news that relates to the role
        
        4. **Know When to Move On**
           - If you don't receive a response after 2-3 follow-ups, focus on other opportunities
           - Keep the door open for future possibilities
        
        5. **Keep Track of All Communications**
           - Update the application status in the tracker after sending follow-ups
           - Document any responses you receive
        """)
