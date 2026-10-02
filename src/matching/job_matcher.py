from matching.jobs_database import JOBS


def match_jobs(resume_skills):

    matched_jobs = []

    # Flatten resume skills into a single set
    user_skills = set()

    for skills in resume_skills.values():
        user_skills.update(skills)

    for job_title, job_data in JOBS.items():

        required_skills = job_data["required_skills"]

        matched_skills = []
        missing_skills = []

        matched_weight = 0
        total_weight = sum(required_skills.values())

        for skill, weight in required_skills.items():

            if skill in user_skills:

                matched_skills.append(skill)
                matched_weight += weight

            else:

                missing_skills.append(skill)

        match_score = round(
            (matched_weight / total_weight) * 100,
            2
        )

        matched_jobs.append({

            "job_title": job_title,

            "category": job_data["category"],

            "experience": job_data["experience"],

            "description": job_data["description"],

            "match_score": match_score,

            "matched_skills": sorted(matched_skills),

            "missing_skills": sorted(missing_skills),

            "matched_weight": matched_weight,

            "total_weight": total_weight

        })

    matched_jobs.sort(

        key=lambda job: job["match_score"],

        reverse=True

    )

    return matched_jobs