from flask import Flask, render_template, request
import os
from pipeline import process_resumes

app = Flask(__name__)

UPLOAD_FOLDER = "resumes"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create folders automatically
os.makedirs("resumes", exist_ok=True)
os.makedirs("output", exist_ok=True)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/upload", methods=["POST"])
def upload_resume():
    file = request.files.get("resume")
    job_desc = request.form.get("jd")   # 🔥 Correct Name (html से match)

    if file.filename == "":
        return "No resume selected!"

    save_path = os.path.join(app.config["UPLOAD_FOLDER"], file.filename)
    file.save(save_path)

    df = process_resumes("resumes", job_desc)
    df.to_csv("output/results.csv", index=False)

    return render_template("result.html", data=df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(debug=True, port=5001)
