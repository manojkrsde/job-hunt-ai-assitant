from crewai import Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.config import GEMINI_API_KEY

# Initialize the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash",
    google_api_key=GEMINI_API_KEY
)

def get_jd_analyst_agent():
    """
    Returns a CrewAI Agent designed to analyze job descriptions.
    """
    return Agent(
        role="Job Description Analyst",
        goal="Analyze job descriptions to extract key responsibilities, skills, and qualifications.",
        backstory=(
            "You are an expert HR specialist and job analyst. "
            "Your strength lies in dissecting complex job postings to identify "
            "what employers are truly looking for."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

def create_jd_analysis_task(agent, job_description):
    """
    Creates a Task for the JD Analyst agent to analyze a specific job description.
    """
    return Task(
        description=(
            f"Analyze the following job description:\n\n{job_description}\n\n"
            "Extract the following details:\n"
            "1. Job Title\n"
            "2. Key Responsibilities (summarized)\n"
            "3. Required Skills & Qualifications\n"
            "4. Remote/Location Details\n"
            "5. Salary Range (if available)"
        ),
        expected_output=(
            "A structured markdown summary of the job description covering "
            "Responsibilities, Skills, and other key details."
        ),
        agent=agent,
        output_file="data/report.md"
    )
