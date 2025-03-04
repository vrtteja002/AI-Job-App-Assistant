import streamlit as st
import os
import json
from datetime import datetime
from core.jobsearch import GoogleJobsSearch, SimulatedJobSearch
from utils.helpers import ensure_directory_exists, save_text_to_file

def show_job_search_page():
    """Display the job search page"""
    st.title("🔍 Job Search")
    
    # Job search form
    st.subheader("Search for Jobs")
    col1, col2, col3 = st.columns([2, 2, 1])
    
    with col1:
        search_query = st.text_input("Job Title or Keywords", "Software Engineer")
    
    with col2:
        location = st.text_input("Location", "Remote")
    
    with col3:
        num_results = st.number_input("Results", min_value=1, max_value=50, value=10)
    
    # Search source selector
    search_source = st.radio(
        "Search Source",
        ["I will be adding (LinkedIn/Indeed)API in future", "Simulated (Demo)"],
        horizontal=True
    )
    
    if st.button("Search Jobs"):
        with st.spinner("Searching for jobs..."):
            # Convert the search source to the appropriate search type
            # Choose which search implementation to use based on selection
            if search_source == "Google Jobs":
                job_search = GoogleJobsSearch()
            else:
               job_search = SimulatedJobSearch()

            # Use the job search implementation directly
            results = job_search.search_jobs(search_query, location, num_results)
            
            st.session_state.search_results = results
            
            # Save results to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"job_search_{timestamp}.json"
            file_path = os.path.join("data", "job_listings", filename)
            ensure_directory_exists(os.path.dirname(file_path))
            save_text_to_file(json.dumps(results, indent=2), file_path)
    
    # Display search results
    if 'search_results' in st.session_state and st.session_state.search_results:
        st.subheader(f"Found {len(st.session_state.search_results['results'])} Jobs")
        
        # Allow sorting options
        sort_option = st.selectbox(
            "Sort by",
            ["Most Recent", "Company Name", "Job Title"]
        )
        
        # Sort results based on selection
        results = st.session_state.search_results['results'].copy()
        if sort_option == "Most Recent":
            results.sort(key=lambda x: x.get('posted_date', ''), reverse=True)
        elif sort_option == "Company Name":
            results.sort(key=lambda x: x.get('company', ''))
        elif sort_option == "Job Title":
            results.sort(key=lambda x: x.get('title', ''))
        
        # Display jobs
        for i, job in enumerate(results):
            with st.expander(f"{job['title']} at {job['company']} - {job['location']}"):
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"**Company:** {job['company']}")
                    st.markdown(f"**Location:** {job['location']}")
                    st.markdown(f"**Posted:** {job.get('posted_date', 'Recently')}")
                    st.markdown(f"**Source:** {job.get('source', 'Unknown')}")
                    
                    if 'salary_range' in job:
                        st.markdown(f"**Salary Range:** {job['salary_range']}")
                    
                    st.markdown("### Description")
                    st.write(job['description'])
                    
                    if 'requirements' in job and job['requirements']:
                        st.markdown("### Requirements")
                        for req in job['requirements']:
                            st.markdown(f"- {req}")
                    
                    if 'application_url' in job:
                        st.markdown(f"[Apply Now]({job['application_url']})")
                
                with col2:
                    api_key = os.getenv("OPENAI_API_KEY")
                    
                    if st.button("Analyze Job", key=f"analyze_{i}"):
                        if not api_key:
                            st.error("Please enter your OpenAI API key in the sidebar first.")
                        elif not st.session_state.resume_loaded:
                            st.error("Please upload your resume first.")
                        else:
                            with st.spinner("Analyzing job..."):
                                st.session_state.job_description = job['description']
                                if 'requirements' in job and job['requirements']:
                                    st.session_state.job_description += "\n\nRequirements:\n" + "\n".join([f"- {req}" for req in job['requirements']])
                                    
                                st.session_state.job_analysis = st.session_state.automator.analyze_job_description(
                                    st.session_state.job_description
                                )
                                
                                # Store company and job title for use in document generation
                                st.session_state.company_name = job['company']
                                st.session_state.position_title = job['title']
                                
                                st.success("Job analyzed! Go to Application Documents to generate a cover letter.")
                    
                    if st.button("Track Application", key=f"track_{i}"):
                        # Load application tracker
                        try:
                            st.session_state.automator.load_application_tracker("data/application_tracker.csv")
                        except:
                            # If file doesn't exist yet, that's fine
                            pass
                            
                        # Track application
                        st.session_state.automator.track_application(job['company'], job['title'])
                        
                        # Save tracker
                        st.session_state.automator.save_application_tracker("data/application_tracker.csv")
                        st.success(f"Application for {job['title']} at {job['company']} tracked successfully.")
    
    # Tips for searching
    with st.expander("Job Search Tips"):
        st.markdown("""
        ### Tips for Effective Job Searching
        
        1. **Use Specific Keywords**
           - Include specific skills, technologies, or job titles
           - Try different variations (e.g., "Developer" vs "Engineer")
        
        2. **Consider Remote Options**
           - Enter "Remote" in the location field to find work-from-home positions
           - Or specify a city name for local opportunities
        
        3. **Analyze Before Applying**
           - Use the "Analyze Job" button to see how well your skills match
           - Check requirements carefully before applying
        
        4. **Track Your Applications**
           - Use the "Track Application" button to keep records of where you've applied
           - Monitor status in the Application Tracker section
        """)