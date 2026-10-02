RECOMMENDATIONS = {
    "Docker": "Learn Docker fundamentals and containerize one project.",
    "Flask": "Build at least one REST API using Flask.",
    "Django": "Develop a Django project such as a blog or e-commerce website.",
    "Spring": "Learn the Spring Framework for Java backend development.",
    "TensorFlow": "Complete a beginner TensorFlow project.",
    "PyTorch": "Build a deep learning project using PyTorch.",
    "Scikit-learn": "Practice classical machine learning algorithms using Scikit-learn.",
    "NumPy": "Strengthen your NumPy fundamentals for data analysis and ML.",
    "Pandas": "Learn data cleaning and analysis using Pandas.",
    "Matplotlib": "Practice data visualization with Matplotlib."
}


def generate_recommendations(job):

    recommendations = []

    for skill in job["missing_skills"]:

        if skill in RECOMMENDATIONS:
            recommendations.append(RECOMMENDATIONS[skill])

        else:
            recommendations.append(
                f"Improve your knowledge of {skill}."
            )

    return recommendations