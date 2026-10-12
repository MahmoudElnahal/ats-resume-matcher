import re
from datetime import datetime
from typing import Optional

def extract_years_of_experience(text: str) -> Optional[int]:
    """
    Estimate the total years of experience from the resume text.

    Looks for patterns like:
    - "2018 - 2021"
    - "Jan 2020 to Present"
    - "5 years of experience"

    Returns:
        int: estimated years of experience, or None if not found
    """
    current_year = datetime.now().year
    total_years = 0
    seen_ranges = set()

    # Match date ranges like "2018 - 2021" or "2019 to present"
    date_matches = re.findall(
        r'(\d{4})\s*(?:-|–|to)\s*(\d{4}|present|now)', text, flags=re.IGNORECASE
    )

    for start, end in date_matches:
        try:
            start_year = int(start)
            end_year = current_year if end.lower() in ['present', 'now'] else int(end)

            if 1950 <= start_year <= end_year <= current_year and (start_year, end_year) not in seen_ranges:
                total_years += (end_year - start_year)
                seen_ranges.add((start_year, end_year))
        except Exception as e:
            continue

    # Match phrases like "5 years of experience"
    explicit_years = re.findall(
        r'(\d+)\+?\s+(?:years|yrs)\s+(?:of\s+)?experience', text, flags=re.IGNORECASE
    )
    for y in explicit_years:
        try:
            total_years += int(y)
        except:
            continue

    return total_years if total_years > 0 else None
