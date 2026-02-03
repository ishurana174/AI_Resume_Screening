import os
import pandas as pd
from extract import extract_resume
from scorer import calculate_similarity

def process_resumes(folder, job_desc):
    results = []

    for file in os.listdir(folder):
        path = os.path.join(folder, file)
        text = extract_resume(path)

        if not text.strip():
            continue

        score = calculate_similarity(text, job_desc)
        results.append({"Resume": file, "Match Score": score})

    return pd.DataFrame(results)
