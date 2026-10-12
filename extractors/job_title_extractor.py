import re
from typing import Optional


COMMON_JOB_TITLES = [
    "Data Analyst", "Data Scientist", "Machine Learning Engineer", "Business Analyst",
    "Software Engineer", "Backend Developer", "Frontend Developer",
    "Data Engineer", "Power BI Developer", "BI Analyst", "Accountant",
    "Project Manager", "Marketing Specialist", "HR Manager"
]

def extract_job_title(text: str) -> Optional[str]:
    """
    Tries to extract the most relevant job title from the resume text.
    """
    text_lower = text.lower()
    for title in COMMON_JOB_TITLES:
        if title.lower() in text_lower:
            return title
    return None
