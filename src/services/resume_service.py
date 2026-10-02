import pdfplumber

from parser.pdf_parser import extract_text_from_pdf
from parser.docx_parser import extract_text_from_docx
from extraction.skill_extractor import extract_skills
from matching.job_matcher import match_jobs
from scoring.resume_analyzer import analyze_resume as analyze_resume_structure
from scoring.resume_scorer import calculate_resume_score
from recommendation.recommendation_engine import generate_recommendations
from models.classifier import predict_resume_category
from analysis.resume_suggestions import generate_resume_suggestions

def analyze_resume(file_path):

    if file_path.lower().endswith(".pdf"):

        resume_text = extract_text_from_pdf(file_path)

        with pdfplumber.open(file_path) as pdf:
            total_pages = len(pdf.pages)

    elif file_path.lower().endswith(".docx"):

        resume_text = extract_text_from_docx(file_path)

        # Word documents don't have fixed pages like PDFs
        total_pages = 1

    else:
        raise ValueError("Unsupported file format")
    
    resume_stats = {
    "pages": total_pages,
    "words": len(resume_text.split()),
    "characters": len(resume_text),
}

    category = predict_resume_category(resume_text)

    skills = extract_skills(resume_text)
    resume_stats["skills_found"] = sum(
        len(skill_list) for skill_list in skills.values()
)
    analysis = analyze_resume_structure(resume_text)

    jobs = match_jobs(skills)

    suggestions = generate_resume_suggestions(
    analysis,
    jobs,
    skills
)

    for job in jobs:

        job["resume_score"] = calculate_resume_score(
            job,
            analysis
        )

        job["recommendations"] = generate_recommendations(job)

    return {
    "resume_text": resume_text,
    "category": category,
    "skills": skills,
    "analysis": analysis,
    "jobs": jobs,
    "resume_stats": resume_stats,
    "suggestions": suggestions
}