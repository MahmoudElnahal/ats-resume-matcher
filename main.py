from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import List
from processor import ResumeProcessor
from matcher import JobMatcher

app = FastAPI(title="Resume Matcher API", version="1.1.0")

processor = ResumeProcessor()

@app.post("/match-cvs")
async def match_cvs(
    job_description: str = Form(...),
    files: List[UploadFile] = File(...)
):
    results = []
    errors = []
    matcher = JobMatcher(job_description)

    for uploaded_file in files:
        try:
            file_bytes = await uploaded_file.read()
            resume = processor.process_pdf_bytes(file_bytes, file_name=uploaded_file.filename)

            if not resume:
                errors.append({"file": uploaded_file.filename, "error": "Resume processing failed."})
                continue

            score, matched_skills, suggestions, extra_info = matcher.match_resume(resume)

            result = {
                "name": resume.name or "-",
                "file_name": resume.file_name,
                "job_title": resume.job_title or "-",
                "location": resume.location or "-",
                "email": resume.email or "-",
                "phone": resume.contact_number or "-",
                "yoe": extra_info.get("yoe", resume.yoe or 0),
                "score": score,
                "final_decision": "✅ مقبول" if score >= 50 else "❌ مرفوض",
                "matched_skills": matched_skills or [],
                "extra_skills": extra_info.get("extra_skills", []),
                "certificates": extra_info.get("certificates", []),
                "projects": extra_info.get("projects", []),
                "suggested_roles": suggestions or [],
                "verdict": extra_info.get("verdict", "-"),
                "summary": resume.summary or "-",
                "graduation_status": extra_info.get("graduation_status", "-"),
                "graduation_year": extra_info.get("graduation_year", "-"),
                "degree": extra_info.get("degree", "-"),
                "last_job": extra_info.get("last_job", "-")
            }

            results.append(result)

        except Exception as e:
            errors.append({"file": uploaded_file.filename, "error": str(e)})

    # ترتيب المقبولين حسب الدرجة تنازليًا
    results = sorted(results, key=lambda x: x["score"], reverse=True)

    return JSONResponse(content={"results": results, "errors": errors})
