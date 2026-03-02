from crewai import Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.config import GEMINI_API_KEY

# Initialize the LLM
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash", 
    google_api_key=GEMINI_API_KEY,
    temperature=0.7
)

def get_messaging_agent():
    """
    Returns a CrewAI Agent designed to write outreach messages.
    """
    return Agent(
        role="Professional Networker & Communications Specialist",
        goal="Draft concise and effective outreach messages to recruiters and hiring managers.",
        backstory=(
            "You are an expert in networking communication. "
            "You know how to craft short, impactful messages that get responses "
            "on platforms like LinkedIn or via email."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

def create_messaging_task(agent, job_summary, agency_name, user_bio=""):
    """
    Creates a Task to generate a professional outreach message.
    """
    return Task(
        description=(
            f"Job Summary: {job_summary}\n"
            f"Agency/Company: {agency_name}\n"
            f"Candidate Bio: {user_bio}\n\n"
            "Task: Write a brief, professional outreach message to a hiring manager or recruiter at this agency.\n"
            "1. Express clear interest in the specific role.\n"
            "2. Mention one key alignment between the candidate's background and the job.\n"
            "3. Keep the tone professional but approachable.\n"
            "4. The message must be suitable for LinkedIn or a direct email introduction.\n"
            "5. Keep it under 150 words."
        ),
        expected_output=(
            "A single, concise outreach message text (under 150 words) ready to be sent."
        ),
        agent=agent
    )
