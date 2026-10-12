import re

# Common world languages — you can expand this list
COMMON_LANGUAGES = [
    "english", "arabic", "french", "german", "spanish", "italian", "russian",
    "chinese", "mandarin", "japanese", "korean", "urdu", "hindi", "turkish", "portuguese"
]

def extract_languages(text: str) -> list:
    """
    Extracts known languages from resume text.

    Args:
        text (str): Resume content

    Returns:
        list: List of detected languages
    """
    text_lower = text.lower()
    found = []

    for lang in COMMON_LANGUAGES:
        if re.search(rf'\b{re.escape(lang)}\b', text_lower):
            found.append(lang.capitalize())

    return sorted(set(found))
    