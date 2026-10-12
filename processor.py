from models import Resume
from utils.pdf_reader import extract_text_from_pdf_bytes
from llm_service import call_gpt
from extractors.birthdate_extractor import extract_birthdate
from extractors.graduation_extractor import extract_graduation
from extractors.job_title_extractor import extract_job_title
from extractors.language_extractor import extract_languages
from extractors.skills_extractor import extract_skills
from extractors.summary_extractor import extract_summary
from extractors.yoe_extractor import extract_years_of_experience
import json

class ResumeProcessor:
    def build_prompt(self, text: str) -> str:
        return f"""
You are a professional resume parser. Extract the following structured fields as valid JSON:
- name
- email
- contact_number
- skills
- education (list with institution, degree, location, start_date, end_date if available)
- experience (list with company, role, location, start_date, end_date)
- summary
- location
- linkedin
- github
- graduated (true/false)
- graduation_year
- degree
- yoe (years of experience)
- languages
- certifications
- projects
- birthdate
- job_title

Only return the raw JSON output. Resume text:
{text}
"""

    def process_pdf_bytes(self, pdf_bytes: bytes, file_name: str = None) -> Resume:
        try:
            text = extract_text_from_pdf_bytes(pdf_bytes)
            if not text.strip():
                print("❌ الملف فارغ أو لا يحتوي على نص.")
                return None

            prompt = self.build_prompt(text)
            response = call_gpt(prompt)

            if not response or not response.strip():
                print("❌ الرد من GPT كان فارغ.")
                return None

            cleaned = response.replace("```json", "").replace("```", "").strip()

            try:
                data = json.loads(cleaned)
            except json.JSONDecodeError:
                print("❌ فشل في تحويل الرد إلى JSON صالح.")
                data = {}

            # 🛠️ Fallbacks
            if not data.get("birthdate"):
                data["birthdate"] = extract_birthdate(text)
            if not data.get("yoe"):
                data["yoe"] = extract_years_of_experience(text)
            if not data.get("job_title"):
                data["job_title"] = extract_job_title(text)
            if not data.get("languages"):
                data["languages"] = extract_languages(text)
            if not data.get("skills"):
                data["skills"] = extract_skills(text)
            if not data.get("summary"):
                data["summary"] = extract_summary(text)

            # 🟢 معالجة التخرج
            graduation_info = extract_graduation(text)
            if graduation_info:
                data.setdefault("graduated", graduation_info.get("status", "Unknown"))
                data.setdefault("graduation_year", graduation_info.get("year", None))
                data.setdefault("degree", graduation_info.get("degree", None))
            else:
                data.setdefault("graduated", "Unknown")
                data.setdefault("graduation_year", None)
                data.setdefault("degree", None)

            # ✅ إصلاح skills إذا dict
            if isinstance(data.get("skills"), dict):
                all_skills = []
                for k in data["skills"].values():
                    if isinstance(k, list):
                        all_skills.extend(k)
                data["skills"] = all_skills

            # ✅ إصلاح yoe
            try:
                data["yoe"] = float(data.get("yoe")) if data.get("yoe") not in [None, ""] else 0.0
            except:
                data["yoe"] = 0.0

            # ✅ Fix certifications
            certs = []
            for c in data.get("certifications", []) or []:
                if isinstance(c, dict) and "title" in c:
                    certs.append(c)
                elif isinstance(c, str):
                    certs.append({"title": c})
            data["certifications"] = certs

            # ✅ Fix languages
            langs = []
            for l in data.get("languages", []) or []:
                if isinstance(l, dict) and "language" in l:
                    langs.append(l)
                elif isinstance(l, str):
                    if "(" in l and ")" in l:
                        lang_name = l.split("(")[0].strip()
                        level = l.split("(")[1].replace(")", "").strip()
                        langs.append({"language": lang_name, "level": level})
                    else:
                        langs.append({"language": l, "level": None})
            data["languages"] = langs

            # ✅ Fix projects
            projects = []
            for p in data.get("projects", []) or []:
                if isinstance(p, dict) and "name" in p:
                    projects.append(p)
                elif isinstance(p, str):
                    projects.append({"name": p})
            data["projects"] = projects

            # ✅ تأمين باقي القوائم
            for field in ["skills", "languages", "certifications", "projects", "experience", "education"]:
                if data.get(field) is None:
                    data[field] = []

            # 🏷️ إضافة اسم الملف
            data["file_name"] = file_name

            # إنشاء Resume
            resume = Resume(**data)
            resume.full_text = text

            return resume

        except Exception as e:
            print(f"❌ Error processing resume: {e}")
            return None
