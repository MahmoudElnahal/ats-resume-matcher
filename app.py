import streamlit as st
import pandas as pd
import io
from processor import ResumeProcessor
from matcher import JobMatcher
from streamlit_extras.add_vertical_space import add_vertical_space

st.set_page_config(page_title="Resume Matcher - وزارة العمل", layout="wide")

if "stage" not in st.session_state:
    st.session_state.stage = "upload"
if "files" not in st.session_state:
    st.session_state.files = []

st.title("📄 نظام تقييم السير الذاتية - وزارة العمل العمانية")
st.caption("تم التطوير بواسطة شركة تقنيات النجاح")

if st.session_state.stage == "upload":
    uploaded_files = st.file_uploader(
        "⬆️ قم بتحميل السير الذاتية (PDF فقط)",
        type=["pdf"],
        accept_multiple_files=True
    )

    st.markdown("---")
    job_text = st.text_area("📝 أدخل وصف الوظيفة هنا", height=250)
    top_n = st.number_input("🔢 عدد المرشحين الأعلى لإظهارهم:", min_value=1, max_value=100, value=5)

    if uploaded_files and job_text:
        st.session_state.files = uploaded_files
        st.session_state.job_text = job_text
        st.session_state.top_n = top_n
        st.session_state.stage = "results"
        st.rerun()

elif st.session_state.stage == "results":
    st.subheader("📊 نتائج التقييم")
    results = []
    rejected = []
    processor = ResumeProcessor()
    matcher = JobMatcher(st.session_state.job_text)

    for uploaded_file in st.session_state.files:
        with st.spinner(f"📂 معالجة: {uploaded_file.name}"):
            file_bytes = uploaded_file.read()
            try:
                result = processor.process_pdf_bytes(file_bytes, file_name=uploaded_file.name)
                if result:
                    score, matched_skills, suggestions, extra_info = matcher.match_resume(result)

                    all_skills = result.skills or []
                    extra_skills = extra_info.get("extra_skills", [])
                    certs = extra_info.get("certificates", [])
                    projects = extra_info.get("projects", [])
                    verdict = extra_info.get("verdict", "")
                    job_title = result.job_title or "-"
                    email = result.email or "-"
                    phone = result.contact_number or result.phone or "-"
                    location = result.location or "-"
                    exp_summary = result.summary or "-"
                    yoe = extra_info.get("yoe") or result.yoe or 0
                    graduation_status = extra_info.get("graduation_status", "-")
                    graduation_year = extra_info.get("graduation_year", "-")
                    degree = extra_info.get("degree", "-")
                    last_job = extra_info.get("last_job", "-")

                    classification = "✅ مقبول" if score >= 50 else "❌ مرفوض"

                    candidate = {
                        "Name": result.name or "-",
                        "File": uploaded_file.name,
                        "Score": score,
                        "YOE": yoe,
                        "Matched Skills": matched_skills,
                        "Extra Skills": extra_skills,
                        "Certificates": certs,
                        "Projects": projects,
                        "Suggested Roles": suggestions,
                        "Final Decision": classification,
                        "Explanation": verdict,
                        "Category": "Junior" if float(yoe) < 2 else "Mid" if float(yoe) < 6 else "Senior",
                        "Email": email,
                        "Phone": phone,
                        "Job Title": job_title,
                        "Location": location,
                        "Experience Summary": exp_summary,
                        "Graduation": f"{graduation_status} - {degree} ({graduation_year})",
                        "Last Job": last_job,
                    }

                    results.append(candidate)
                else:
                    rejected.append((uploaded_file.name, "⚠️ السيرة الذاتية فارغة أو غير قابلة للقراءة."))
            except Exception as e:
                rejected.append((uploaded_file.name, str(e)))

    df_all = pd.DataFrame(results)
    if "Score" in df_all.columns:
        df_all = df_all.sort_values(by="Score", ascending=False)

    if not df_all.empty:
        st.markdown("## 👥 تفاصيل المرشحين")
        for candidate in results:
            with st.expander(f"📌 {candidate['Name']} - {candidate['Category']}"):
                col1, col2 = st.columns([1, 1])
                with col1:
                    st.markdown(f"**🗂️ اسم الملف:** `{candidate['File']}`")
                    st.markdown(f"**🏷️ المسمى الوظيفي:** {candidate['Job Title']}")
                    st.markdown(f"**📍 الموقع:** {candidate['Location']}")
                    st.markdown(f"**📧 البريد الإلكتروني:** {candidate['Email']}")
                    st.markdown(f"**📱 الهاتف:** {candidate['Phone']}")
                    st.markdown(f"**🎓 الخبرة (سنوات):** {candidate['YOE']}")
                    st.markdown(f"**🎓 التعليم:** {candidate['Graduation']}")
                    st.markdown(f"**💼 آخر وظيفة:** {candidate['Last Job']}")
                    st.markdown(f"**🔢 الدرجة:** `{candidate['Score']}`")
                    st.markdown(f"**🏁 القرار النهائي:** {candidate['Final Decision']}")
                with col2:
                    st.markdown("✅ **المهارات المطابقة:**")
                    st.success(", ".join(candidate["Matched Skills"]) or "-")
                    st.markdown("🛠️ **المهارات الإضافية:**")
                    st.info(", ".join(candidate["Extra Skills"]) or "-")
                    st.markdown("📂 **الشهادات:**")
                    st.info(", ".join(candidate["Certificates"]) or "-")
                    st.markdown("💡 **المشاريع:**")
                    st.code("\n".join(candidate["Projects"]) or "-", language="markdown")

                st.markdown("🧠 **الشرح والتحليل:**")
                st.info(candidate["Explanation"] or "-")

                st.markdown("🧾 **ملخص الخبرات:**")
                st.write(candidate["Experience Summary"])

        # 📥 زر تحميل النتائج
        output = io.BytesIO()
        df_export = pd.DataFrame([{
            "Name": c["Name"],
            "Score": c["Score"],
            "YOE": c["YOE"],
            "Job Title": c["Job Title"],
            "Email": c["Email"],
            "Phone": c["Phone"],
            "Matched Skills": ", ".join(c["Matched Skills"]),
            "Extra Skills": ", ".join(c["Extra Skills"]),
            "Certificates": ", ".join(c["Certificates"]),
            "Projects": "; ".join(c["Projects"]),
            "Verdict": c["Explanation"],
            "Decision": c["Final Decision"],
            "Graduation": c["Graduation"],
            "Last Job": c["Last Job"]
        } for c in results])
        df_export.to_excel(output, index=False, engine="openpyxl")
        output.seek(0)
        st.download_button("⬇️ تحميل النتائج بصيغة Excel", output, "results.xlsx")

    if rejected:
        st.markdown("## ⚠️ ملفات لم تتم معالجتها:")
        for filename, reason in rejected:
            st.warning(f"{filename}: {reason}")

    # 🔁 إعادة التشغيل
    add_vertical_space(1)
    if st.button("🔁 بدء من جديد"):
        st.session_state.stage = "upload"
        st.session_state.files = []
        st.rerun()
