import os
import csv
from datetime import datetime

def save_cover_letter_file(content):
    """
    Creates a timestamped .txt file for each cover letter and saves it to the data/cover_letters/ directory.
    """
    directory = os.path.join("data", "cover_letters")
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(directory, f"cover_letter_{timestamp}.txt")
    
    with open(filename, "w", encoding='utf-8') as f:
        f.write(content)
    
    return filename

def log_application(job_title, agency, resume_summary):
    """
    Logs key application details into data/applications_log.csv.
    """
    directory = "data"
    if not os.path.exists(directory):
        os.makedirs(directory)

    log_file = os.path.join(directory, "applications_log.csv")
    file_exists = os.path.isfile(log_file)
    
    with open(log_file, "a", newline="", encoding='utf-8') as csvfile:
        fieldnames = ["timestamp", "job_title", "agency", "resume_summary"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if not file_exists:
            writer.writeheader()
            
        writer.writerow({
            "timestamp": datetime.now().isoformat(),
            "job_title": job_title,
            "agency": agency,
            "resume_summary": resume_summary
        })
