from crewai import Agent, Task
from langchain_google_genai import ChatGoogleGenerativeAI
from utils.config import GEMINI_API_KEY

# Initialize the LLM with a slightly higher temperature for creativity
llm = ChatGoogleGenerativeAI(
    model="gemini/gemini-3.1-flash-lite-preview",
    google_api_key=GEMINI_API_KEY,
    temperature=0.7
)

def get_resume_cl_agent():
    """
    Returns a CrewAI Agent designed to tailor resumes and write cover letters.
    """
    return Agent(
        role="Career Coach & Resume Writer",
        goal="Tailor resumes and write compelling cover letters to match job descriptions.",
        backstory=(
            "You are an expert career coach who specializes in government and corporate recruitment. "
            "You know exactly how to highlight a candidate's strengths to match specific job requirements."
        ),
        llm=llm,
        verbose=True,
        allow_delegation=False
    )

def create_resume_cl_task(agent, job_summary, resume_text):
    """
    Creates a Task to generate a tailored resume summary and cover letter.
    """
    return Task(
        description=(
            f"Job Summary:\n{job_summary}\n\n"
            f"Candidate Resume:\n{resume_text}\n\n"
            "Your task is to:\n"
            "1. Rewrite the candidate's resume summary to specifically align with the job's key responsibilities and skills.\n"
            "2. Write a professional, personalized cover letter addressing the hiring manager. Emphasize why the candidate is a perfect fit.\n\n"
            "IMPORTANT: Output your response using the following format EXACTLY with these markers:\n\n"
            "<<RESUME_SUMMARY>>\n"
            "[Insert Tailored Resume Summary Here]\n"
            "\n"
            "<<COVER_LETTER>>\n"
            "[Insert Full Cover Letter Here]"
        ),
        expected_output=(
            "A text output containing the tailored resume summary and cover letter, "
            "clearly separated by the specified markers."
        ),
        agent=agent,
        output_file="data/resume_agent_output.txt"
    )
