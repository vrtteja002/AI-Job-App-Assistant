import streamlit as st
import pandas as pd
import json
from datetime import datetime

def get_download_link(text, filename, link_text):
    """
    Generate a download link for text content
    """
    import base64
    b64 = base64.b64encode(text.encode()).decode()
    href = f'<a href="data:file/txt;base64,{b64}" download="{filename}">{link_text}</a>'
    return href

def display_json(json_data, key=None):
    """
    Nicely display JSON data with option to expand/collapse
    """
    try:
        if isinstance(json_data, str):
            data = json.loads(json_data)
        else:
            data = json_data
            
        st.json(data)
    except:
        st.text_area("Raw Data", json_data, height=300, key=key)

def generate_filename(prefix, company=None, position=None, extension="txt"):
    """
    Generate a consistent filename with timestamp
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if company and position:
        company_name = company.replace(' ', '_').lower()
        position_name = position.replace(' ', '_').lower()
        filename = f"{prefix}_{company_name}_{position_name}_{timestamp}.{extension}"
    else:
        filename = f"{prefix}_{timestamp}.{extension}"
        
    return filename

def save_and_provide_download(content, prefix, company=None, position=None, extension="txt"):
    """
    Save content to a file and provide a download button
    """
    import os
    from utils.helpers import ensure_directory_exists
    
    filename = generate_filename(prefix, company, position, extension)
    output_path = os.path.join("outputs", filename)
    
    # Ensure directory exists
    ensure_directory_exists(os.path.dirname(output_path))
    
    # Save to file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Provide download button
    with open(output_path, "r", encoding='utf-8') as f:
        st.download_button(
            label=f"Download {prefix.replace('_', ' ').title()}",
            data=f,
            file_name=filename,
            mime=f"text/{extension}"
        )
        
    return output_path

def display_application_statistics(application_tracker):
    """
    Display application statistics with metrics and charts
    """
    # Get statistics
    stats = application_tracker.get_application_statistics()
    
    # Display metrics
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Applications", stats['total_applications'])
    with col2:
        applied_count = stats['status_counts'].get('Applied', 0)
        st.metric("Applications Pending", applied_count)
    with col3:
        interview_count = stats['status_counts'].get('Interview Scheduled', 0)
        st.metric("Interviews Scheduled", interview_count)
    
    # If we have application data, show charts
    if stats['total_applications'] > 0:
        # Status breakdown chart
        st.subheader("Application Status Breakdown")
        status_df = pd.DataFrame(list(stats['status_counts'].items()), 
                                columns=['Status', 'Count'])
        st.bar_chart(status_df.set_index('Status'))
        
        # Application timeline if enough data
        applications = application_tracker.get_all_applications()
        if len(applications) >= 3:
            st.subheader("Application Timeline")
            
            # Convert dates to datetime
            applications['date_applied'] = pd.to_datetime(applications['date_applied'])
            
            # Group by week and count
            timeline = applications.groupby(pd.Grouper(key='date_applied', freq='W')).size().reset_index(name='count')
            timeline['date_applied'] = timeline['date_applied'].dt.strftime('%Y-%m-%d')
            
            st.line_chart(timeline.set_index('date_applied'))

def display_job_match_score(match_score, company, position):
    """
    Display job match score with visualization
    """
    try:
        # Try to parse as JSON
        if isinstance(match_score, str):
            match_data = json.loads(match_score)
        else:
            match_data = match_score
            
        # Extract overall score
        overall_score = match_data.get('overall_match_score', 0)
        
        # Create a gauge chart-like display
        st.subheader(f"Match Score: {company} - {position}")
        
        # Display overall score
        col1, col2 = st.columns([1, 3])
        with col1:
            st.markdown(f"### {overall_score}%")
        with col2:
            # Create a progress bar
            st.progress(overall_score / 100)
            
            # Add color indicator
            if overall_score >= 80:
                st.success("Excellent Match")
            elif overall_score >= 60:
                st.info("Good Match")
            elif overall_score >= 40:
                st.warning("Fair Match")
            else:
                st.error("Poor Match")
        
        # Display score breakdown
        if 'score_breakdown' in match_data:
            st.subheader("Score Breakdown")
            breakdown = match_data['score_breakdown']
            
            for category, score in breakdown.items():
                st.caption(f"{category.title()}: {score}%")
                st.progress(score / 100)
        
        # Display strengths and weaknesses
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Strengths")
            strengths = match_data.get('strongest_matching_points', [])
            for strength in strengths:
                st.markdown(f"- {strength}")
                
        with col2:
            st.subheader("Areas to Improve")
            weaknesses = match_data.get('areas_for_improvement', [])
            for weakness in weaknesses:
                st.markdown(f"- {weakness}")
        
        # Display talking points for interview
        if 'suggested_talking_points' in match_data:
            st.subheader("Suggested Talking Points")
            talking_points = match_data['suggested_talking_points']
            for point in talking_points:
                st.markdown(f"- {point}")
                
    except Exception as e:
        # If we can't parse as JSON, just display as text
        st.text_area("Match Analysis", match_score, height=300)
