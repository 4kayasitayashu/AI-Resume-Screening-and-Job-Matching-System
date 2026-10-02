from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
)


# ==========================================================
# STYLES
# ==========================================================

styles = getSampleStyleSheet()

title_style = styles["Title"]
title_style.alignment = TA_CENTER
title_style.spaceAfter = 20

heading_style = styles["Heading2"]
heading_style.textColor = colors.HexColor("#0F4C81")
heading_style.spaceBefore = 12
heading_style.spaceAfter = 8

normal_style = styles["BodyText"]
normal_style.spaceAfter = 5

bullet_style = styles["BodyText"]
bullet_style.leftIndent = 18
bullet_style.spaceAfter = 3


# ==========================================================
# FOOTER
# ==========================================================

def draw_footer(canvas, doc):

    canvas.saveState()

    canvas.setFont("Helvetica", 9)

    canvas.setFillColor(colors.grey)

    canvas.drawString(
        inch,
        0.45 * inch,
        "AI Resume Screening & Job Matching System"
    )

    canvas.drawRightString(
        doc.width + doc.leftMargin,
        0.45 * inch,
        f"Page {doc.page}"
    )

    canvas.restoreState()


# ==========================================================
# EXECUTIVE SUMMARY TABLE
# ==========================================================

def build_summary_table(category, jobs):

    best_job = max(
        jobs,
        key=lambda job: job["match_score"],
        default=None
    )

    data = [
        ["Resume Category", category.replace("-", " ").title()],
        ["Jobs Matched", str(len(jobs))],
        ["Best Career Match", best_job["job_title"] if best_job else "N/A"],
        ["Highest Match Score", f"{best_job['match_score']:.2f}%" if best_job else "N/A"]
    ]

    table = Table(
        data,
        colWidths=[190, 220]
    )

    table.setStyle(

        TableStyle([

            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#E8F0FE")),

            ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),

            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),

            ("BOTTOMPADDING", (0, 0), (-1, -1), 8),

            ("TOPPADDING", (0, 0), (-1, -1), 8),

            ("VALIGN", (0, 0), (-1, -1), "MIDDLE")

        ])

    )

    return table


# ==========================================================
# SECTION HEADING
# ==========================================================

def add_heading(story, text):

    story.append(
        Paragraph(
            text,
            heading_style
        )
    )

    story.append(
        Spacer(
            1,
            0.08 * inch
        )
    )


# ==========================================================
# HORIZONTAL DIVIDER
# ==========================================================

def add_divider(story):

    table = Table(
        [[""]],
        colWidths=[430],
        rowHeights=[1]
    )

    table.setStyle(

        TableStyle([

            ("LINEBELOW", (0, 0), (-1, -1), 1, colors.lightgrey)

        ])

    )

    story.append(table)

    story.append(
        Spacer(
            1,
            0.12 * inch
        )
    )


# ==========================================================
# BOOLEAN FORMATTER
# ==========================================================

def format_boolean(text, value):

    if value:
        return f"✓ {text}"

    return f"✗ {text}"

# ==========================================================
# HEADER
# ==========================================================

def build_header(story):

    story.append(
        Paragraph(
            "AI Resume Screening & Job Matching Report",
            title_style
        )
    )

    story.append(
        Paragraph(
            f"Generated on: {datetime.now().strftime('%d %B %Y, %I:%M %p')}",
            normal_style
        )
    )

    story.append(
        Spacer(
            1,
            0.25 * inch
        )
    )


# ==========================================================
# EXECUTIVE SUMMARY
# ==========================================================

def build_summary_section(story, result):

    add_heading(
        story,
        "Executive Summary"
    )

    story.append(

        build_summary_table(

            result["category"],

            result["jobs"]

        )

    )

    story.append(

        Spacer(
            1,
            0.25 * inch
        )

    )


# ==========================================================
# TOP SKILLS (QUICK REPORT)
# ==========================================================

def build_top_skills_section(story, result):

    add_heading(
        story,
        "Top Skills"
    )

    skills = result["skills"]

    top_skills = []

    for values in skills.values():
        top_skills.extend(values)

    top_skills = top_skills[:10]

    if not top_skills:

        story.append(
            Paragraph(
                "No skills detected.",
                normal_style
            )
        )

        return

    for skill in top_skills:

        story.append(
            Paragraph(
                f"• {skill}",
                bullet_style
            )
        )

    story.append(
        Spacer(
            1,
            0.20 * inch
        )
    )


# ==========================================================
# SKILLS SECTION
# ==========================================================

def build_skills_section(story, result):

    add_heading(
        story,
        "Extracted Skills"
    )

    skills = result["skills"]

    for category, values in skills.items():

        if not values:
            continue

        story.append(
            Paragraph(
                f"<b>{category}</b>",
                normal_style
            )
        )

        for skill in sorted(values):

            story.append(
                Paragraph(
                    f"• {skill}",
                    bullet_style
                )
            )

        story.append(
            Spacer(
                1,
                0.10 * inch
            )
        )


# ==========================================================
# RESUME ANALYSIS
# ==========================================================

def build_analysis_section(story, result):

    add_heading(
        story,
        "Resume Analysis"
    )

    analysis = result["analysis"]

    mapping = [

        ("Email Found", analysis["has_email"]),

        ("Phone Number Found", analysis["has_phone"]),

        ("Projects Section Found", analysis["has_projects"]),

        ("Education Section Found", analysis["has_education"]),

        ("Certifications Found", analysis["has_certifications"])

    ]

    for text, value in mapping:

        story.append(

            Paragraph(

                format_boolean(
                    text,
                    value
                ),

                normal_style

            )

        )

    story.append(

        Spacer(
            1,
            0.20 * inch
        )

    )

# ==========================================================
# JOB RECOMMENDATIONS
# ==========================================================

def build_jobs_section(story, result):

    add_heading(
        story,
        "Recommended Jobs"
    )

    jobs = sorted(
        result["jobs"],
        key=lambda x: x["match_score"],
        reverse=True
    )

    for index, job in enumerate(jobs, start=1):

        # ---------------------------------
        # Job Title
        # ---------------------------------

        story.append(
            Paragraph(
                f"<b>{index}. {job['job_title']}</b>",
                styles["Heading3"]
            )
        )

        # ---------------------------------
        # Scores Table
        # ---------------------------------

        score_table = Table(
            [
                ["Match Score", f"{job['match_score']:.2f}%"],
                ["Resume Score", f"{job['resume_score']:.2f}/100"],
            ],
            colWidths=[170, 120]
        )

        score_table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F2F7FF")),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
            ])
        )

        story.append(score_table)

        story.append(
            Spacer(
                1,
                0.12 * inch
            )
        )

        # ---------------------------------
        # Matched Skills
        # ---------------------------------

        matched = job.get("matched_skills", [])

        if matched:

            story.append(
                Paragraph(
                    "<b>Matched Skills</b>",
                    normal_style
                )
            )

            for skill in sorted(matched):

                story.append(
                    Paragraph(
                        f"✓ {skill}",
                        bullet_style
                    )
                )

        story.append(
            Spacer(
                1,
                0.08 * inch
            )
        )

        # ---------------------------------
        # Missing Skills
        # ---------------------------------

        missing = job.get("missing_skills", [])

        if missing:

            story.append(
                Paragraph(
                    "<b>Missing Skills</b>",
                    normal_style
                )
            )

            for skill in sorted(missing):

                story.append(
                    Paragraph(
                        f"• {skill}",
                        bullet_style
                    )
                )

        story.append(
            Spacer(
                1,
                0.08 * inch
            )
        )

        # ---------------------------------
        # Recommendations
        # ---------------------------------

        recommendations = job.get("recommendations", [])

        if recommendations:

            story.append(
                Paragraph(
                    "<b>Recommendations</b>",
                    normal_style
                )
            )

            for rec in recommendations:

                story.append(
                    Paragraph(
                        f"• {rec}",
                        bullet_style
                    )
                )

        story.append(
            Spacer(
                1,
                0.15 * inch
            )
        )

        add_divider(story)



# ==========================================================
# RESUME IMPROVEMENT SUGGESTIONS
# ==========================================================

def build_top_jobs_section(story, result):

    add_heading(
        story,
        "Top Career Matches"
    )

    jobs = sorted(
        result["jobs"],
        key=lambda x: x["match_score"],
        reverse=True
    )[:5]

    if not jobs:

        story.append(
            Paragraph(
                "No matching jobs found.",
                normal_style
            )
        )
        return

    data = [["Job Role", "Match Score"]]

    for job in jobs:

        data.append([
            job["job_title"],
            f"{job['match_score']:.2f}%"
        ])

    table = Table(
        data,
        colWidths=[4.5 * inch, 1.5 * inch]
    )

    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1F4E78")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 8),
        ("ALIGN", (1, 1), (-1, -1), "CENTER"),
    ]))

    story.append(table)
    story.append(Spacer(1, 0.2 * inch))


def build_suggestions_section(story, result):

    add_heading(
        story,
        "Resume Improvement Suggestions"
    )

    suggestions = result.get("suggestions", [])

    if not suggestions:

        story.append(
            Paragraph(
                "No suggestions available.",
                normal_style
            )
        )

        return

    for suggestion in suggestions:

        story.append(
            Paragraph(
                f"✓ {suggestion}",
                bullet_style
            )
        )

    story.append(
        Spacer(
            1,
            0.20 * inch
        )
    )

# ==========================================================
# MAIN PDF GENERATOR
# ==========================================================

def generate_pdf_report(result, output_path, report_type="quick"):

    doc = SimpleDocTemplate(
        output_path,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=50
    )

    story = []

    # ------------------------------------------------------
    # Header
    # ------------------------------------------------------

    build_header(story)

    # ------------------------------------------------------
    # Executive Summary
    # ------------------------------------------------------

    build_summary_section(
    story,
    result
)

    add_divider(story)

    if report_type == "quick":

        build_top_skills_section(
            story,
            result
        )

        add_divider(story)

        build_top_jobs_section(
            story,
            result
        )

        add_divider(story)

    else:

        build_skills_section(
            story,
            result
        )

        add_divider(story)

        build_analysis_section(
            story,
            result
        )

        add_divider(story)

        build_jobs_section(
            story,
            result
        )

        add_divider(story)

    build_suggestions_section(
        story,
        result
    )

    add_divider(story)


    # ------------------------------------------------------
    # Footer
    # ------------------------------------------------------

    story.append(
        Spacer(
            1,
            0.25 * inch
        )
    )

    story.append(
        Paragraph(
            "<font color='grey'><i>"
            "Generated by AI Resume Screening & Job Matching System"
            "</i></font>",
            normal_style
        )
    )

    doc.build(
        story,
        onFirstPage=draw_footer,
        onLaterPages=draw_footer
    )