from models import Resume
from llm_service import call_gpt
import json

class JobMatcher:
    def __init__(self, job_description: str):
        self.job_description = job_description

    def match_resume(self, resume: Resume) -> tuple[int, list[str], list[str], dict]:
        resume_text = resume.full_text or resume.summary or ""
        if not resume_text.strip():
            return 0, [], [], {"verdict": "⚠️ السيرة الذاتية فارغة"}

        # 🧠 برومبت مُحسَّن للتحليل
        prompt = f"""
أنت خبير توظيف وتحليل سير ذاتية.

📌 وصف الوظيفة:
\"\"\"{self.job_description}\"\"\"

📄 السيرة الذاتية:
\"\"\"{resume_text}\"\"\"

⬇️ المطلوب:
1. قيّم مدى مناسبة المرشح لهذه الوظيفة من 0 إلى 100
2. استخرج المهارات المطابقة (matched_skills)
3. استخرج المهارات الإضافية (extra_skills) — المهارات المذكورة في السيرة ولكن غير مطابقة للوصف
4. اقترح أدوار محتملة للمرشح (suggested_roles)
5. حدد حالة التخرج: Graduate أو Undergraduate
6. سنة التخرج إن وجدت
7. آخر وظيفة أو تدريب قام به (last_job)
8. اشرح بالتفصيل سبب القبول أو الرفض مع ذكر أمثلة من سيرته الذاتية ومقارنتها بمتطلبات الوظيفة

🎯 ارسل الرد كـ JSON بالهيكل التالي:
{{
  "score": 85,
  "matched_skills": ["Skill1", "Skill2"],
  "extra_skills": ["OtherSkill1", "OtherSkill2"],
  "suggested_roles": ["Role A", "Role B"],
  "graduation_info": {{
    "status": "Graduate",
    "year": 2023,
    "degree": "Computer Science"
  }},
  "last_job": "Data Analyst Intern at XYZ Company",
  "verdict": "مناسب جدًا بسبب تطابق المهارات الأساسية مثل SQL وPower BI مع متطلبات الوظيفة."
}}
"""

        try:
            response = call_gpt(prompt)
            cleaned = response.replace("```json", "").replace("```", "").strip()
            parsed = json.loads(cleaned)

            score = int(parsed.get("score", 0))
            matched_skills = parsed.get("matched_skills", []) or []
            extra_skills = parsed.get("extra_skills", []) or []
            suggestions = parsed.get("suggested_roles", [])
            verdict = parsed.get("verdict", "-")

            graduation_info = parsed.get("graduation_info", {})
            last_job = parsed.get("last_job", "-")

            # fallback للـ matched skills لو GPT مرجعش
            if not matched_skills and resume.skills:
                matched_skills = [
                    skill for skill in resume.skills
                    if skill.lower() in self.job_description.lower()
                ]

            # بناء الـ extra info
            extra_info = {
                "verdict": verdict,
                "yoe": resume.yoe,
                "certificates": [c.title for c in resume.certifications] if resume.certifications else [],
                "projects": [p.name for p in resume.projects] if resume.projects else [],
                "extra_skills": extra_skills,
                "graduation_status": graduation_info.get("status", "-"),
                "graduation_year": graduation_info.get("year", "-"),
                "degree": graduation_info.get("degree", "-"),
                "last_job": last_job,
            }

            return score, matched_skills, suggestions, extra_info

        except Exception as e:
            return 0, [], [], {"verdict": f"❌ فشل في التحليل: {e}"}
