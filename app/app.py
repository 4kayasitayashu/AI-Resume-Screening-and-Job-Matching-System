import os
import sys
import tempfile
import streamlit as st
import pandas as pd
import plotly.express as px


# Add src directory to Python path
sys.path.append(os.path.abspath("src"))

from services.resume_service import analyze_resume
from reports.pdf_report import generate_pdf_report

st.set_page_config(
    page_title="AI Resume Screening & Job Matching",
    page_icon="📄",
    layout="wide",   
    initial_sidebar_state="expanded"
)
st.markdown(
    """
    <style>
    /* Hide Streamlit anchor link icons */
    a[href^="#"] {
        display: none !important;
    }

    /* Hide heading anchor icons */
    .stHeadingAnchor {
        display: none !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.title("📄 AI Resume Screening")

st.sidebar.info(
    """
This application uses Machine Learning and NLP to:

- Classify resumes
- Extract technical skills
- Analyse resume quality
- Match suitable job roles
- Calculate resume scores
- Generate recommendations
"""
)

st.sidebar.divider()

st.sidebar.success("Supported Format: PDF or DOCX")



st.title("📄 AI Resume Screening & Job Matching System")
st.divider()
st.markdown(
    """
Upload your resume in **PDF** format to:

- Predict your resume category
- Extract technical skills
- Analyse your resume
- Match suitable job roles
- Calculate a resume score
- Get personalized recommendations
"""
)

st.divider()

uploaded_file = st.file_uploader(
    "Upload Resume (PDF or DOCX)",
    type=["pdf", "docx"]
)

def display_job(job):

    match = job["match_score"]

    if match >= 90:
        badge = "🟢 Excellent Match"
    elif match >= 75:
        badge = "🟡 Good Match"
    elif match >= 60:
        badge = "🟠 Moderate Match"
    else:
        badge = "🔴 Low Match"

    with st.expander(
        f"🏆 {job['job_title']} | {match:.2f}% | {badge}"
):

        info1, info2 = st.columns(2)

        with info1:
            st.info(f"**Category**\n\n{job['category']}")

        with info2:
            st.info(f"**Experience**\n\n{job['experience']}")

        st.write("### 📝 Job Description")
        st.write(job["description"])

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.metric(
                "Match Score",
                f"{job['match_score']:.2f}%"
            )

        with col2:
            st.metric(
                "Skill Weight",
                f"{job['matched_weight']} / {job['total_weight']}"
            )

        st.progress(job["match_score"] / 100)

        if match >= 90:
            st.success(
                "Your resume is an excellent fit for this role."
            )

        elif match >= 75:
            st.info(
                "Your resume matches this role well. Learning a few additional skills could improve your chances."
            )

        elif match >= 60:
            st.warning(
                "You have a moderate match. Consider strengthening the missing skills."
            )

        else:
            st.error(
                "Your current profile is not a strong fit for this role."
            )

        st.write(
            f"### ✅ Matched Skills ({len(job['matched_skills'])})"
        )

        if job["matched_skills"]:
            for skill in job["matched_skills"]:
                st.success(skill)
        else:
            st.info("No matched skills found.")

        st.write(
            f"### ❌ Missing Skills ({len(job['missing_skills'])})"
        )

        if job["missing_skills"]:
            for skill in job["missing_skills"]:
                st.error(skill)
        else:
            st.success("No missing skills.")

if uploaded_file is not None:

    st.success(f"Uploaded: {uploaded_file.name}")

    if st.button("🚀 Analyse Resume", width="stretch"):

        with st.spinner("Analysing resume..."):

            file_extension = os.path.splitext(uploaded_file.name)[1]

            with tempfile.NamedTemporaryFile(
                delete=False,
                suffix=file_extension
            ) as tmp:
                tmp.write(uploaded_file.read())
                temp_path = tmp.name

            try:
                result = analyze_resume(temp_path)

                st.session_state["result"] = result

                st.success("Analysis completed successfully!")

            except Exception as e:
                st.error(f"Error: {e}")

            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)

if "result" in st.session_state:

    result = st.session_state["result"]


    import io

    # -----------------------------
    # Quick Report
    # -----------------------------

    quick_pdf_buffer = io.BytesIO()

    generate_pdf_report(
        result,
        quick_pdf_buffer,
        report_type="quick"
    )

    quick_pdf_buffer.seek(0)

    # -----------------------------
    # Detailed Report
    # -----------------------------

    detailed_pdf_buffer = io.BytesIO()

    generate_pdf_report(
        result,
        detailed_pdf_buffer,
        report_type="detailed"
    )

    detailed_pdf_buffer.seek(0)

    st.divider()

    st.header("📊 Resume Analysis Report")
    best_job = max(
    result["jobs"],
    key=lambda job: job["match_score"]
)

    stats = result["resume_stats"]    

    with st.container(border=True):

        st.subheader("📋 Resume Overview")

        st.divider()

        col1, col2 = st.columns(2)

        with col1:
            st.metric("📂 Category", result["category"].replace("-", " ").title())
            st.metric("📄 Pages", stats["pages"])
            st.metric("🛠 Skills Found", stats["skills_found"])

        with col2:
            st.metric("📝 Words", stats["words"])
            st.metric("🎯 Top Recommended Role", best_job["job_title"])
            st.metric("🎯 Best Match", f"{best_job['match_score']:.2f}%")

    best_job = max(
    result["jobs"],
    key=lambda job: job["match_score"]
)

    with st.container(border=True):

        st.subheader("🛠️ Extracted Skills")

        st.divider()

        skills = result["skills"]

        total_categories = sum(
        1 for skill_list in skills.values() if skill_list
    )

        total_skills = sum(
            len(skill_list) for skill_list in skills.values()
        )

        st.caption(
            f"Detected **{total_skills}** skills across **{total_categories}** categories."
        )

        st.write("")

        col1, col2 = st.columns(2)

        items = list(skills.items())

        for i, (category, skill_list) in enumerate(items):

            if not skill_list:
                continue

            with col1 if i % 2 == 0 else col2:

                st.caption("────────────────────────")
                st.markdown(f"**📂 {category}**")
                st.caption("────────────────────────")

                for skill in skill_list:
                    st.markdown(
                        f"<div style='margin-left:25px;'>✅ {skill}</div>",
                        unsafe_allow_html=True
                    )

                st.write("")

    with st.container(border=True):

        st.subheader("📋 Resume Analysis")

        st.divider()

        analysis = result["analysis"]

        analysis_items = [
            ("Email Found", analysis["has_email"]),
            ("Phone Number Found", analysis["has_phone"]),
            ("Projects Section Found", analysis["has_projects"]),
            ("Education Section Found", analysis["has_education"]),
            ("Certifications Found", analysis["has_certifications"]),
        ]

        col1, col2 = st.columns(2)

        for i, (label, status) in enumerate(analysis_items):

            with col1 if i % 2 == 0 else col2:

                if status:
                    st.success(f"✅ {label}")
                else:
                    st.error(f"❌ {label}")

    with st.container(border=True):
    
        st.subheader("🏆 Top Job Recommendations")
        st.caption("Jobs ranked by overall skill match.")
        st.divider()
        jobs = result["jobs"]

        jobs = sorted(
            jobs,
            key=lambda x: x["match_score"],
            reverse=True
        )

        top_jobs = jobs[:5]
        remaining_jobs = jobs[5:]

        best_job = top_jobs[0]

        st.subheader("🌟 Best Career Match")
        st.caption(
            "Based on your skills, experience and resume analysis."
        )

        with st.container(border=True):

            st.markdown(f"## 🏆 {best_job['job_title']}")

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Match Score",
                    f"{best_job['match_score']:.2f}%"
                )

            with col2:
                st.metric(
                    "Matched Skills",
                    len(best_job["matched_skills"])
                )

            with col3:
                st.metric(
                    "Missing Skills",
                    len(best_job["missing_skills"])
                )

            st.progress(best_job["match_score"] / 100)

            st.write("### Why this role?")

            if best_job["matched_skills"]:
                top_skills = ", ".join(best_job["matched_skills"][:5])

                st.info(
                    f"Your resume strongly matches this role because it contains **{top_skills}**."
                )

            if best_job["missing_skills"]:
                st.warning(
                    "Learning **"
                    + ", ".join(best_job["missing_skills"][:3])
                    + "** could improve your match even further."
                )
        st.divider()

        # Show Top 5 Jobs
        for job in top_jobs[1:5]:
            display_job(job)


        # Show Remaining Jobs inside an Expander
        if remaining_jobs:

            with st.expander(
                f"📂 Show Remaining {len(remaining_jobs)} Job Profiles"
            ):

                for job in remaining_jobs:
                    display_job(job)

    st.divider()

    with st.container(border=True):

        st.subheader("💡 Resume Improvement Suggestions")

        st.divider()

        suggestions = result["suggestions"]

        with st.container(border=True):

            for suggestion in suggestions:
                st.write(f"✅ {suggestion}")

    with st.container(border=True):

        st.subheader("📊 Job Match Comparison")

        st.divider()

        chart_data = pd.DataFrame({
            "Job Role": [job["job_title"] for job in jobs],
            "Match Score": [job["match_score"] for job in jobs]
        })

        fig = px.bar(
        chart_data,
        x="Job Role",
        y="Match Score",
        text="Match Score",
    )

        fig.update_traces(texttemplate="%{text:.2f}%", textposition="outside")

        fig.update_layout(
            yaxis=dict(range=[0, 100]),
            xaxis_title="",
            yaxis_title="Match Score (%)"
        )

        st.plotly_chart(fig, width="stretch")

    with st.container(border=True):

        st.subheader("📈 Resume Skills Summary")

        st.divider()

        skills_summary = pd.DataFrame({
            "Category": list(skills.keys()),
            "Count": [len(v) for v in skills.values()]
        })

        skills_summary = skills_summary[
            skills_summary["Count"] > 0
        ]

        fig = px.pie(
            skills_summary,
            names="Category",
            values="Count",
            hole=0.45
        )

        fig.update_traces(
            textinfo="label+percent"
        )

        st.plotly_chart(
            fig,
            width="stretch"
    )

    with st.container(border=True):

        st.subheader("📄 Download Reports")

        st.caption(
            "Choose the report format that best suits your needs."
        )

        st.divider()

        col1, col2 = st.columns(2)

        with col1:

            st.markdown("### 📄 Quick Report")
            st.caption(
                "Includes the key insights and top recommendations."
            )

            st.download_button(
                label="⬇ Download Quick Report",
                data=quick_pdf_buffer,
                file_name="resume_quick_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

        with col2:

            st.markdown("### 📘 Detailed Report")
            st.caption(
                "Complete resume analysis with all extracted information."
            )

            st.download_button(
                label="⬇ Download Detailed Report",
                data=detailed_pdf_buffer,
                file_name="resume_detailed_report.pdf",
                mime="application/pdf",
                use_container_width=True
            )

    st.divider()

    st.caption(
        "Developed by Shivansh Srivastava | AI Resume Screening & Job Matching System"
)