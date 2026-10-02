def generate_resume_suggestions(analysis, jobs, skills):

    suggestions = []

    # -----------------------------
    # Resume Sections
    # -----------------------------

    if not analysis["has_email"]:
        suggestions.append(
            "Add a professional email address to your resume."
        )

    if not analysis["has_phone"]:
        suggestions.append(
            "Include your contact number."
        )

    if not analysis["has_projects"]:
        suggestions.append(
            "Add a Projects section to showcase your practical experience."
        )

    if not analysis["has_education"]:
        suggestions.append(
            "Include an Education section."
        )

    if not analysis["has_certifications"]:
        suggestions.append(
            "Add relevant certifications to strengthen your profile."
        )

    # -----------------------------
    # Skill-based Suggestions
    # -----------------------------

    if jobs:

        best_job = max(
            jobs,
            key=lambda job: job["match_score"]
        )

        missing_skills = best_job["missing_skills"][:5]

        if missing_skills:

            for skill in missing_skills:
                suggestions.append(
                    f"Learn **{skill}** to improve your match for the **{best_job['job_title']}** role."
                )

    # -----------------------------
    # Overall Skills
    # -----------------------------

    total_skills = sum(
        len(skill_list)
        for skill_list in skills.values()
    )

    if total_skills < 10:
        suggestions.append(
            "Try adding more technical skills relevant to your target job."
        )

    return suggestions