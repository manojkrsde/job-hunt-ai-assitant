import sys
import os
import re
from crewai import Crew, Process
from agents.jd_analyst import get_jd_analyst_agent, create_jd_analysis_task
from agents.resume_cl_agent import get_resume_cl_agent, create_resume_cl_task
from agents.messaging_agent import get_messaging_agent, create_messaging_task
from usajobs_api import fetch_usajobs
from utils.tracking import log_application, save_cover_letter_file

def load_resume():
    """Reads the sample resume text from data/sample_resume.txt."""
    resume_path = os.path.join("data", "sample_resume.txt")
    if not os.path.exists(resume_path):
        return "No resume found."
    with open(resume_path, "r", encoding="utf-8") as f:
        return f.read()

def extract_between_markers(text, start_marker, end_marker=None):
    """
    Extracts text between start_marker and end_marker.
    If end_marker is None, extracts until the end of the string.
    """
    try:
        start_idx = text.find(start_marker)
        if start_idx == -1:
            return ""
        start_idx += len(start_marker)
        
        if end_marker:
            end_idx = text.find(end_marker, start_idx)
            if end_idx == -1:
                return text[start_idx:].strip()
            return text[start_idx:end_idx].strip()
        else:
            return text[start_idx:].strip()
    except Exception as e:
        print(f"Error extracting text: {e}")
        return ""

def run_pipeline(job_data, resume_text, user_bio):
    """
    Analyzes a specific job, and generates a tailored resume/CL and outreach message.
    Args:
        job_data (dict): The job posting object.
        resume_text (str): Candidate's resume.
        user_bio (str): Candidate's bio.
    """
    
    # Extract Job Summary
    try:
        descriptor = job_data.get('MatchedObjectDescriptor', {})
        details = descriptor.get('UserArea', {}).get('Details', {})
        job_summary = details.get('JobSummary')
        
        # Extract additional fields for messaging & logging
        agency_name = descriptor.get('OrganizationName', 'the hiring agency')
        job_title = descriptor.get('PositionTitle', 'the position')

        if not job_summary:
             job_summary = f"Title: {job_title}\n" \
                           f"Summary: {details.get('JobOverview') or str(job_data)}"
            
    except Exception as e:
        print(f"Error extracting job summary: {e}")
        job_summary = str(job_data)
        agency_name = "the agency"
        job_title = "Unknown"

    # Initialize Agents
    analyst_agent = get_jd_analyst_agent()
    resume_agent = get_resume_cl_agent()
    messaging_agent = get_messaging_agent()

    # Create Tasks
    analysis_task = create_jd_analysis_task(analyst_agent, job_summary)
    resume_task = create_resume_cl_task(resume_agent, job_summary, resume_text)
    messaging_task = create_messaging_task(messaging_agent, job_summary, agency_name, user_bio)

    # Create and run the Crew
    crew = Crew(
        agents=[analyst_agent, resume_agent, messaging_agent],
        tasks=[analysis_task, resume_task, messaging_task],
        process=Process.sequential,
        max_rpm=10  # To avoid hitting API rate limits, adjust as needed based on your API quotas, or set to None for no limit
    )

    result = crew.kickoff()

    try:
        # 1. Manually grab the output from all tasks
        analyst_output = str(analysis_task.output)
        resume_agent_output = str(resume_task.output)
        messaging_output = str(messaging_task.output)
        
        # 2. Extract specific parts for logging
        resume_summary = extract_between_markers(resume_agent_output, "<<RESUME_SUMMARY>>", "<<COVER_LETTER>>")
        cover_letter = extract_between_markers(resume_agent_output, "<<COVER_LETTER>>")
        
        # 3. Log the application
        if resume_summary:
             cleaned_summary = resume_summary[:200] + "..." if len(resume_summary) > 200 else resume_summary
             log_application(job_title, agency_name, cleaned_summary)
        
        # 4. Save the cover letter
        if cover_letter:
            file_path = save_cover_letter_file(cover_letter)
            print(f"Cover letter saved to: {file_path}")
            
    except Exception as e:
        print(f"Error saving/logging application data: {e}")

    return {
        "analysis": analyst_output,
        "resume_summary": resume_summary if resume_summary else "*(Could not extract summary accurately. See raw output.)*\n\n" + resume_agent_output,
        "cover_letter": cover_letter if cover_letter else "*(Could not extract cover letter accurately. See raw output.)*\n\n" + resume_agent_output,
        "messaging": messaging_output
    }


if __name__ == "__main__":
    print("This script is designed to be run from the Streamlit app.")
