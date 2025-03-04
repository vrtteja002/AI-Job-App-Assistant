import streamlit as st
import os
from datetime import datetime
import sys

# Add the project root to Python's path if needed
if not any(p.endswith('job_track') for p in sys.path):
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config import APP_STATUS

def show_tracker_page():
    """Display the application tracker page"""
    st.title("📊 Application Tracker")
    
    # Initialize tracker if needed
    try:
        st.session_state.automator.load_application_tracker("data/application_tracker.csv")
        applications = st.session_state.automator.application_tracker.get_all_applications()
    except Exception as e:
        # If file doesn't exist yet, create an empty tracker
        st.session_state.automator.application_tracker.save_tracker("data/application_tracker.csv")
        applications = st.session_state.automator.application_tracker.get_all_applications()
    
    # Add new application form
    with st.expander("Add New Application"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_company = st.text_input("Company Name")
            new_position = st.text_input("Position Title")
        
        with col2:
            new_status = st.selectbox("Status", list(APP_STATUS.values()))
            new_notes = st.text_area("Notes", height=100)
        
        if st.button("Add Application"):
            if not new_company or not new_position:
                st.error("Please enter company name and position title.")
            else:
                # Track application
                st.session_state.automator.track_application(new_company, new_position, new_status, new_notes)
                
                # Save tracker
                st.session_state.automator.save_application_tracker("data/application_tracker.csv")
                st.success(f"Application for {new_position} at {new_company} tracked successfully.")
                st.rerun()
    
    # Display applications
    if not applications.empty:
        # Filter by status
        status_filter = st.selectbox("Filter by Status", ["All"] + list(APP_STATUS.values()))
        
        if status_filter != "All":
            filtered_applications = applications[applications['status'] == status_filter]
        else:
            filtered_applications = applications
        
        # Show statistics
        stats = st.session_state.automator.application_tracker.get_application_statistics()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Applications", stats['total_applications'])
        with col2:
            applied_count = stats['status_counts'].get('Applied', 0)
            st.metric("Applications Pending", applied_count)
        with col3:
            interview_count = stats['status_counts'].get('Interview Scheduled', 0)
            st.metric("Interviews Scheduled", interview_count)
        
        # Display table of applications
        st.subheader(f"Applications ({len(filtered_applications)})")
        
        # Convert DataFrame to display
        display_df = filtered_applications[['company', 'position', 'date_applied', 'status', 'follow_up_date']]
        st.dataframe(display_df)
        
        # Detailed view of applications
        st.subheader("Application Details")
        for i, app in filtered_applications.iterrows():
            with st.expander(f"{app['position']} at {app['company']}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Applied:** {app['date_applied']}")
                    st.markdown(f"**Status:** {app['status']}")
                    st.markdown(f"**Follow-up Due:** {app['follow_up_date']}")
                    
                    if app['contact_person']:
                        st.markdown(f"**Contact:** {app['contact_person']}")
                    
                    if app['contact_email']:
                        st.markdown(f"**Email:** {app['contact_email']}")
                    
                    if app['notes']:
                        st.markdown("**Notes:**")
                        st.text_area("", app['notes'], key=f"notes_{i}", height=100, disabled=True)
                
                with col2:
                    # Update status
                    new_status = st.selectbox("Update Status", list(APP_STATUS.values()), 
                                             index=list(APP_STATUS.values()).index(app['status']),
                                             key=f"status_{i}")
                    
                    if st.button("Update", key=f"update_{i}"):
                        st.session_state.automator.application_tracker.update_application(
                            app['company'], app['position'], status=new_status
                        )
                        st.session_state.automator.save_application_tracker("data/application_tracker.csv")
                        st.success("Status updated!")
                        st.rerun()
                    
                    if st.button("Generate Follow-up", key=f"followup_{i}"):
                        api_key = os.getenv("OPENAI_API_KEY")
                        if not api_key:
                            st.error("Please enter your OpenAI API key in the sidebar first.")
                        else:
                            st.session_state.selected_company = app['company']
                            st.session_state.selected_position = app['position']
                            st.success("Go to Follow-up Manager to generate the email.")
                            
                    if st.button("Delete", key=f"delete_{i}"):
                        if st.session_state.automator.application_tracker.delete_application(
                            app['company'], app['position']
                        ):
                            st.session_state.automator.save_application_tracker("data/application_tracker.csv")
                            st.success("Application deleted!")
                            st.rerun()
    else:
        st.info("No applications tracked yet. Use the form above to add your first application.")
        
        # Add sample data option
        if st.button("Add Sample Applications (Demo)"):
            # Add sample applications
            samples = [
                {"company": "Tech Innovators Inc.", "position": "Software Engineer", "status": "Applied", 
                 "notes": "Applied through company website. Looking for Python and React expertise."},
                {"company": "DataCrunch Solutions", "position": "Data Scientist", "status": "Interview Scheduled", 
                 "notes": "First interview scheduled for next week. Prepare ML algorithm examples."},
                {"company": "Cloud Nine Computing", "position": "DevOps Engineer", "status": "Follow-up Sent", 
                 "notes": "Sent follow-up email on " + datetime.now().strftime("%Y-%m-%d")},
            ]
            
            for sample in samples:
                st.session_state.automator.track_application(
                    sample["company"], sample["position"], sample["status"], sample["notes"]
                )
            
            st.session_state.automator.save_application_tracker("data/application_tracker.csv")
            st.success("Sample applications added!")
            st.rerun()
