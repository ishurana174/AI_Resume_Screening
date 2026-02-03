from pipeline import process_resumes

job_description = """
Looking for a Python developer with knowledge of Machine Learning, NLP,
Data Analysis, Scikit-Learn, and problem-solving,Python Programming

AI/ML Basics

Intro to NLP.
"""

resume_folder = "../resumes/"
output_file = "../output/results.csv"

df = process_resumes(resume_folder, job_description)
df.to_csv(output_file, index=False)

print("Screening Complete! Check output/results.csv")
print(df)
