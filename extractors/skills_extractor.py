import re
from typing import List


KNOWN_SKILLS = [
    "Python", "SQL", "Power BI", "Excel", "Tableau", "R",
    "Pandas", "NumPy", "Machine Learning", "Deep Learning",
    "Data Analysis", "Data Cleaning", "Data Visualization",
    "ETL", "Power Query", "DAX", "SSIS", "SSRS", "SPSS",
    "Matplotlib", "Seaborn", "Scikit-learn", "Statistics",
    "Communication", "Problem Solving", "Time Management",
    "Leadership", "Critical Thinking", "Teamwork", "VBA"
]

def extract_skills(text: str) -> List[str]:
    """
    Extracts known skills from resume text using keyword matching.
    """
    text_lower = text.lower()
    found_skills = []

    for skill in KNOWN_SKILLS:
        pattern = r"\b" + re.escape(skill.lower()) + r"\b"
        if re.search(pattern, text_lower):
            found_skills.append(skill)

    return list(set(found_skills))  
