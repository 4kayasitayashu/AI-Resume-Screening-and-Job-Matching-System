from extraction.skills_database import SKILLS, ALIASES
import re

# Build alias lookup once
SKILL_ALIASES = {}

for skills in SKILLS.values():
    for skill in skills:
        SKILL_ALIASES[skill] = [skill]

for alias, canonical in ALIASES.items():
    SKILL_ALIASES.setdefault(canonical, []).append(alias)


def extract_skills(resume_text):

    found_skills = {}

    resume_text = resume_text.lower()

    for category, skills in SKILLS.items():

        extracted = set()

        for canonical_skill in skills:

            for search_term in SKILL_ALIASES.get(canonical_skill, []):

                pattern = (
                    r"(?<![A-Za-z0-9])"
                    + re.escape(search_term.lower())
                    + r"(?![A-Za-z0-9])"
)

                if re.search(pattern, resume_text):
                    extracted.add(canonical_skill)
                    break

        if extracted:
            found_skills[category] = sorted(extracted)

    return found_skills