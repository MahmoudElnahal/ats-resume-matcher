import re

def extract_summary(text: str) -> str:
    """
    Extract a professional summary or objective section from resume text.

    Args:
        text (str): Resume content

    Returns:
        str: Extracted summary if found, else empty string
    """
    # Convert to lowercase for pattern detection
    lower_text = text.lower()

    # Possible summary section headers
    summary_keywords = ["summary", "professional summary", "profile", "career objective", "objective"]

    for keyword in summary_keywords:
        match = re.search(rf"{keyword}[\s:]*\n?(.*?)(\n\n|\n[A-Z])", text, re.IGNORECASE | re.DOTALL)
        if match:
            extracted = match.group(1).strip()
            if len(extracted.split()) >= 10:  # at least 10 words to be a real summary
                return extracted

    # Fallback: use first paragraph (before education or experience)
    match = re.split(r"(?i)\b(education|experience|work history|skills|projects)\b", text)
    if match:
        intro = match[0].strip()
        if len(intro.split()) > 20:
            return intro

    return ""
