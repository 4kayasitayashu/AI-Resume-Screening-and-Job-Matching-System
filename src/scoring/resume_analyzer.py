import re


def analyze_resume(resume_text):

    analysis = {
        "has_email": False,
        "has_phone": False,
        "has_projects": False,
        "has_education": False,
        "has_certifications": False
    }

    if re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", resume_text):
        analysis["has_email"] = True

    if re.search(r"\b\d{10}\b", resume_text):
        analysis["has_phone"] = True

    text = resume_text.lower()

    if "project" in text:
        analysis["has_projects"] = True

    if "education" in text:
        analysis["has_education"] = True

    if "certification" in text or "certifications" in text:
        analysis["has_certifications"] = True

    return analysis