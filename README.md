# AI Job Hunt Assistant 🚀

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://job-hunt-assistantgit-zmsajx3uqzqst3y8xuzian.streamlit.app/)

A powerful, AI-driven assistant designed to streamline your job search process. Built with **Python**, **CrewAI**, and **Streamlit**.

## 🔗 Live Demo
Check out the live application here: [**job-hunt-assistant.streamlit.app**](https://job-hunt-assistantgit-zmsajx3uqzqst3y8xuzian.streamlit.app/)

## ✨ Features
- **Job Description Analysis**: Extracts key skills and requirements from JD.
- **Resume Tailoring**: Customizes your resume based on specific job listings.
- **Outreach Messaging**: Drafts personalized messages for networking.
- **USAJobs Integration**: Fetches relevant job openings automatically.

## 🛠️ Tech Stack
- **AI Core**: CrewAI & Gemini (via Google AI Studio)
- **Frontend**: Streamlit
- **API**: USAJobs API

## 🚀 Getting Started

### 1. Prerequisites
- Python 3.10+
- A Google Gemini API Key
- A USAJobs API Key

### 2. Installation
```bash
git clone <your-repo-url>
cd job_hunt_assistant
pip install -r requirements.txt
```

### 3. Configuration
Create a `.env` file in the `utils/` folder with your API keys:
```env
GEMINI_API_KEY="your_key_here"
USAJOBS_API_KEY="your_key_here"
```

### 4. Running the App
```bash
streamlit run app.py
```

## 📜 License
MIT License

