# ATS — LLM Resume Parser & Job Matcher

Upload a batch of PDF resumes and a job description; get back a ranked shortlist with a 0–100 fit score, matched skills, and a written reason for each accept/reject decision.

Built as the prototype for an applicant tracking system for the Ministry of Labor of Oman (Success Technology LLC). The interface and the model's verdicts are in Arabic.

## How it works

```
PDF resumes ──► PyMuPDF text ──► GPT-4o parser ──► Resume (Pydantic)
                                                        │
job description ────────────────────────────────► GPT-4o matcher
                                                        │
                              score · matched/extra skills · suggested roles · verdict
                                                        │
                                   ranked table · accept ≥ 50 · Excel export
```

1. **Parse** — `processor.py` extracts the PDF text and asks the LLM for structured JSON: name, contact details, education, experience, skills, certifications, projects, languages, years of experience.
2. **Fill gaps** — the regex/heuristic extractors in `extractors/` cover fields the LLM missed (birthdate, graduation, job title, languages, skills, summary, years of experience).
3. **Match** — `matcher.py` compares each resume with the job description and returns a score, matched and extra skills, suggested alternative roles, graduation status, last job and a detailed verdict. If the LLM returns no matched skills, it falls back to a keyword match.
4. **Rank** — candidates are sorted by score; 50 and above is marked accepted.

## Two interfaces

| | Run | Use |
|---|---|---|
| **Streamlit app** (`app.py`) | `streamlit run app.py` | Upload resumes, paste the job description, pick top-N, download the results as Excel |
| **FastAPI** (`main.py`) | `uvicorn main:app --reload` | `POST /match-cvs` with `job_description` (form field) and `files` (PDFs); docs at `/docs` |

Example API call:

```bash
curl -X POST http://localhost:8000/match-cvs \
  -F "job_description=$(cat assets/sample_job.txt)" \
  -F "files=@resume1.pdf" -F "files=@resume2.pdf"
```

## Setup

```bash
git clone https://github.com/MahmoudElnahal/ATS.git
cd ATS
python -m venv venv && source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
export OPENAI_API_KEY=your_key                    # Windows: set OPENAI_API_KEY=your_key
```

The key is read from the `OPENAI_API_KEY` environment variable (`config.py`). No resumes are included in this repository — bring your own PDFs.

## Project layout

```
app.py               Streamlit UI
main.py              FastAPI service
processor.py         PDF → structured Resume via LLM
matcher.py           Resume ↔ job description scoring
models.py            Pydantic models
llm_service.py       OpenAI client wrapper
vector_utils.py      Sentence-transformer embeddings + cosine similarity
suggestions_map.py   Skill → suggested role map
extractors/          Fallback field extractors
utils/pdf_reader.py  PyMuPDF text extraction
assets/sample_job.txt
```

## Stack

Python · OpenAI GPT-4o · FastAPI · Streamlit · PyMuPDF · Pydantic · sentence-transformers · scikit-learn · pandas

## Author

[Mahmoud El Nahal](https://github.com/MahmoudElnahal)
