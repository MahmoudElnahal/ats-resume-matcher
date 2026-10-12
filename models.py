from typing import Optional, List
from pydantic import BaseModel, Field

class Education(BaseModel):
    institution: Optional[str]
    degree: Optional[str]
    location: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]

class Experience(BaseModel):
    company: Optional[str]
    role: Optional[str]
    location: Optional[str]
    start_date: Optional[str]
    end_date: Optional[str]

class Project(BaseModel):
    name: Optional[str]
    description: Optional[str] = None

class Certification(BaseModel):
    title: Optional[str]
    link: Optional[str] = None

class Language(BaseModel):
    language: Optional[str]
    level: Optional[str] = None

class Resume(BaseModel):
    name: Optional[str]
    email: Optional[str]
    contact_number: Optional[str]
    phone: Optional[str] = None  # ➕ إضافي لتوافق matcher
    file_name: Optional[str] = None  # ➕ اسم الملف
    skills: Optional[List[str]] = []
    education: Optional[List[Education]] = []
    experience: Optional[List[Experience]] = []
    summary: Optional[str]
    location: Optional[str]
    linkedin: Optional[str]
    github: Optional[str]
    graduated: Optional[bool]
    yoe: Optional[float]
    languages: Optional[List[Language]] = []
    certifications: Optional[List[Certification]] = []
    projects: Optional[List[Project]] = []
    birthdate: Optional[str]
    job_title: Optional[str]
    degree: Optional[str] = None  # ➕ الحقل الناقص
    full_text: Optional[str] = None  # ➕ محتوى كامل النص (ضروري للذكاء الاصطناعي)

    @classmethod
    def parse_with_skip(cls, data: dict) -> "Resume":
        def parse_list_safe(key: str, model):
            parsed_items = []
            for item in data.get(key, []):
                if isinstance(item, dict):
                    try:
                        parsed_items.append(model(**item))
                    except Exception:
                        continue
                elif isinstance(item, str) and key == "projects":
                    parsed_items.append(Project(name=item))
            return parsed_items

        data["projects"] = parse_list_safe("projects", Project)
        data["experience"] = parse_list_safe("experience", Experience)
        data["certifications"] = parse_list_safe("certifications", Certification)
        data["languages"] = parse_list_safe("languages", Language)
        data["education"] = parse_list_safe("education", Education)

        # توحيد رقم الهاتف
        if "contact_number" in data and "phone" not in data:
            data["phone"] = data["contact_number"]

        return cls(**data)
