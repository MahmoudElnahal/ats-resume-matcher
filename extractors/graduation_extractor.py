import re

def extract_graduation(text: str, return_year: bool = False):
    """
    يستخرج بيانات التخرج من النص:
    - Graduate / Undergraduate
    - سنة التخرج إن وجدت
    - اسم الكلية / التخصص
    """
    result = {
        "status": "Unknown",
        "year": None,
        "degree": None
    }

    text_lower = text.lower()

    # 🔹 تحديد الحالة
    if "graduate" in text_lower or "bachelor" in text_lower or "degree" in text_lower:
        result["status"] = "Graduate"
    elif "undergraduate" in text_lower or "student" in text_lower or "currently studying" in text_lower:
        result["status"] = "Undergraduate"

    # 🔹 البحث عن سنة التخرج (أربع أرقام من 1990 إلى 2035)
    year_match = re.search(r"(19|20)\d{2}", text)
    if year_match:
        result["year"] = int(year_match.group())

    # 🔹 استخراج الكلية / التخصص
    degree_match = re.search(
        r"(faculty of [A-Za-z ]+|college of [A-Za-z ]+|bachelor(?:'s)? in [A-Za-z ]+|bsc in [A-Za-z ]+)",
        text,
        re.IGNORECASE
    )
    if degree_match:
        result["degree"] = degree_match.group().strip()

    if return_year:
        return result["year"]

    return result
