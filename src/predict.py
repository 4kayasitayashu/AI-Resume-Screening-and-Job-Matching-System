from services.resume_service import analyze_resume
from reports.pdf_report import generate_pdf_report

def print_results(result):

    print("Predicted Category:")
    print(result["category"])

    print("\nExtracted Skills:")
    print(result["skills"])

    print("\nResume Analysis:")
    print(result["analysis"])

    print("\nRecommended Jobs:")

    for job in result["jobs"]:

        print(f"\nJob: {job['job_title']}")
        print(f"Resume Score: {job['resume_score']}/100")
        print(f"Matched Skills: {job['matched_skills']}")
        print(f"Missing Skills: {job['missing_skills']}")

        print("Recommendations:")

        for recommendation in job["recommendations"]:
            print(f"- {recommendation}")


if __name__ == "__main__":

    result = analyze_resume("resumes/sde.pdf")

    print_results(result)

    generate_pdf_report(
    result,
    "reports/resume_report.pdf"
)

    print("\nPDF report generated successfully!")