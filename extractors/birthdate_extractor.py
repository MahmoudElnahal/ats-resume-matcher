import re
from datetime import datetime

def extract_birthdate(text: str) -> str:
    """
    Attempts to extract a birthdate from resume text.
    Returns date in ISO format (YYYY-MM-DD) if found, otherwise empty string.
    """

    # Common patterns: 01/01/1990, 1990-01-01, January 1st, 1990, etc.
    patterns = [
        r"(\d{1,2}[/-]\d{1,2}[/-](19|20)\d{2})",          # e.g. 01/01/1990 or 01-01-1990
        r"((19|20)\d{2}[/-]\d{1,2}[/-]\d{1,2})",           # e.g. 1990-01-01
        r"(January|February|March|April|May|June|July|August|September|October|November|December)[^\n]{0,15}(19|20)\d{2}",  # e.g. January 1st, 1990
        r"[Dd]ate of birth[:\s]+((19|20)\d{2})",           # DOB: 1990
    ]

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            raw_date = match.group(0)
            # Try parsing to standard format
            for fmt in ("%d/%m/%Y", "%d-%m-%Y", "%Y-%m-%d", "%B %d, %Y", "%B %dst, %Y", "%B %dnd, %Y", "%B %drd, %Y", "%B %dth, %Y"):
                try:
                    parsed = datetime.strptime(raw_date, fmt)
                    return parsed.strftime("%Y-%m-%d")
                except:
                    continue
            return raw_date  # fallback

    return ""
