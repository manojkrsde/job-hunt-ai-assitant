import streamlit as st
import sys
import os
import time

os.environ["CREWAI_DISABLE_TELEMETRY"] = "true"
from crewai import Crew, Process

from agents.jd_analyst import get_jd_analyst_agent, create_jd_analysis_task
from agents.resume_cl_agent import get_resume_cl_agent, create_resume_cl_task
from agents.messaging_agent import get_messaging_agent, create_messaging_task
from usajobs_api import fetch_usajobs
from orchestrator import run_pipeline

# --- Streamlit UI Layout ---
st.set_page_config(page_title="AI Job Hunt Assistant", page_icon="🕵️", layout="wide")

st.title("🕵️ AI Job Hunt Assistant")
st.markdown("""
This tool uses AI agents to help you land your next government job.
1.  **Analyst Agent**: Analyzes the job description.
2.  **Resume Agent**: Tailors your resume and writes a cover letter.
3.  **Messaging Agent**: Drafts a LinkedIn/Email outreach message.
""")

with st.sidebar:
    st.header("Input Parameters")
    job_keyword = st.text_input("Job Keyword", "Data Scientist")
    location = st.text_input("Location", "")
    
    st.markdown("---")
    st.subheader("Your Profile")
    user_bio = st.text_area("Your Bio (Short)", "I am a working professional looking for new opportunities.")
    
    # Pre-load sample resume if available
    try:
        with open("data/sample_resume.txt", "r", encoding="utf-8") as f:
            sample_resume = f.read()
    except:
        sample_resume = ""
        
    resume_text = st.text_area("Your Resume Text", sample_resume, height=300)

# Initialize session state for jobs
if 'jobs_list' not in st.session_state:
    st.session_state.jobs_list = []

# Button to search for jobs
if st.button("Search for Jobs"):
    with st.spinner(f"Fetching '{job_keyword}' jobs..."):
        st.session_state.jobs_list = fetch_usajobs(keyword=job_keyword, location=location, results_per_page=5)
        if not st.session_state.jobs_list:
            st.error("No jobs found. Please check your criteria.")

# Display job selection form if jobs are available
if st.session_state.jobs_list:
    st.divider()
    st.subheader("Select Jobs to Apply For")
    
    selected_indices = []
    
    # Create a form so user can select multiple jobs
    with st.form("job_selection_form"):
        for i, job in enumerate(st.session_state.jobs_list):
            title = job.get('MatchedObjectDescriptor', {}).get('PositionTitle', 'Unknown Title')
            agency = job.get('MatchedObjectDescriptor', {}).get('OrganizationName', 'Unknown Agency')
            
            # Checkbox for each job
            if st.checkbox(f"{title} - {agency}", key=f"job_{i}"):
                selected_indices.append(i)
                
        submit_selection = st.form_submit_button("Run AI Agents on Selected Jobs")
    
    # Process selected jobs
    if submit_selection:
        if not selected_indices:
            st.warning("Please select at least one job.")
        elif not resume_text:
            st.warning("Please provide your resume text.")
        else:
            for index in selected_indices:
                selected_job = st.session_state.jobs_list[index]
                title = selected_job.get('MatchedObjectDescriptor', {}).get('PositionTitle', 'this job')
                
                with st.expander(f"Results for: {title}", expanded=True):
                    with st.spinner(f"Processing application for {title}..."):
                        try:
                            # Call the refactored run_pipeline
                            final_output = run_pipeline(selected_job, resume_text, user_bio)
                            st.markdown(final_output)
                            st.success(f"Completed processing for {title}")

                        except Exception as e:
                            st.error("⚠️ An error occurred while running the AI agents.")
                            if "ImportError" in str(e) and "native provider" in str(e):
                                st.info("This is likely due to a misconfigured LLM model name or a missing dependency in CrewAI. Please check your agent configurations.")
                            else:
                                st.info(f"Details: {e}")
                            st.warning("Please ensure your API keys are correct and the models are accessible.")

                        finally:
                            # --- COOLDOWN TIMER RUNS NO MATTER WHAT ---
                            countdown_placeholder = st.empty() 
                            for seconds in range(60, 0, -1):
                                countdown_placeholder.warning(f"⏳ API Cooldown: Please wait {seconds} seconds to prevent rate limits...")
                                time.sleep(1) 
                            
                            countdown_placeholder.empty() 
                            # ------------------------------------------
