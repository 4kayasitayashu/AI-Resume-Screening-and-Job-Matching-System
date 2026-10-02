from scoring.scoring_weights import SCORING_WEIGHTS


def calculate_resume_score(job, analysis):

    score = job["match_score"]

    if analysis["has_email"]:
        score += SCORING_WEIGHTS["email"]

    if analysis["has_phone"]:
        score += SCORING_WEIGHTS["phone"]

    if analysis["has_projects"]:
        score += SCORING_WEIGHTS["projects"]

    if analysis["has_education"]:
        score += SCORING_WEIGHTS["education"]

    if analysis["has_certifications"]:
        score += SCORING_WEIGHTS["certifications"]

    score = min(score, 100)

    return round(score, 2)