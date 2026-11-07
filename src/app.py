from flask import Flask, render_template, request
import os
import shutil
import tempfile

from pipeline import process_resumes
from extract import extract_resume
from ats_analyzer import analyze_ats


app = Flask(__name__)


# =========================================================
# CONFIGURATION
# =========================================================

UPLOAD_FOLDER = "resumes"
OUTPUT_FOLDER = "output"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# =========================================================
# CREATE REQUIRED FOLDERS
# =========================================================

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():
    return render_template("index.html")


# =========================================================
# RESUME SCANNER
# =========================================================
#
# Resume + Job Description
#        ↓
# Job Match
#        ↓
# ATS Score
#        ↓
# Detailed Result
#
# =========================================================

@app.route("/upload", methods=["POST"])
def upload_resume():

    # -----------------------------------------------------
    # GET RESUME
    # -----------------------------------------------------

    file = request.files.get("resume")

    # -----------------------------------------------------
    # GET JOB DESCRIPTION
    # -----------------------------------------------------

    job_desc = request.form.get("jd", "").strip()

    # -----------------------------------------------------
    # VALIDATE RESUME
    # -----------------------------------------------------

    if not file or file.filename == "":
        return "No resume selected!"

    # -----------------------------------------------------
    # VALIDATE JOB DESCRIPTION
    # -----------------------------------------------------

    if not job_desc:
        return "Please enter a Job Description!"

    # -----------------------------------------------------
    # VALIDATE FILE TYPE
    # -----------------------------------------------------

    filename = os.path.basename(file.filename)

    extension = os.path.splitext(filename)[1].lower()

    if extension not in [".pdf", ".docx"]:
        return "Only PDF and DOCX files are supported!"

    # =====================================================
    # SAVE CURRENT RESUME
    # =====================================================

    save_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        filename
    )

    file.save(save_path)

    # =====================================================
    # TEMPORARY FOLDER
    # =====================================================

    temp_folder = tempfile.mkdtemp(
        prefix="current_resume_"
    )

    try:

        # -------------------------------------------------
        # COPY CURRENT RESUME TO TEMP FOLDER
        # -------------------------------------------------

        temp_resume_path = os.path.join(
            temp_folder,
            filename
        )

        shutil.copy2(
            save_path,
            temp_resume_path
        )

        # =================================================
        # 1. JOB MATCHING
        # =================================================

        df = process_resumes(
            temp_folder,
            job_desc
        )

        # -------------------------------------------------
        # SAVE JOB MATCH RESULT
        # -------------------------------------------------

        df.to_csv(
            os.path.join(
                OUTPUT_FOLDER,
                "results.csv"
            ),
            index=False
        )

        # =================================================
        # 2. EXTRACT RESUME TEXT
        # =================================================

        resume_text = extract_resume(
            save_path
        )

        # =================================================
        # 3. ATS ANALYSIS
        # =================================================

        ats_result = analyze_ats(
            resume_text,
            job_desc
        )

        # =================================================
        # 4. RESULT PAGE
        # =================================================

        return render_template(
            "result.html",
            data=df.to_dict(orient="records"),
            ats=ats_result
        )

    finally:

        # -------------------------------------------------
        # DELETE TEMPORARY FOLDER
        # -------------------------------------------------

        shutil.rmtree(
            temp_folder,
            ignore_errors=True
        )


# =========================================================
# STANDALONE ATS SCORE CHECKER PAGE
# =========================================================
#
# Student / Employee can upload resume
# WITHOUT entering Job Description.
#
# =========================================================

@app.route("/ats-checker")
def ats_checker():

    return render_template(
        "ats_checker.html"
    )


# =========================================================
# STANDALONE ATS SCORE ANALYSIS
# =========================================================
#
# Resume only
#     ↓
# Extract text
#     ↓
# ATS Analyzer
#     ↓
# ATS Score
#     ↓
# Detailed ATS Report
#
# =========================================================

@app.route("/ats-check", methods=["POST"])
def ats_check():

    # -----------------------------------------------------
    # GET RESUME
    # -----------------------------------------------------

    file = request.files.get("resume")

    # -----------------------------------------------------
    # VALIDATE RESUME
    # -----------------------------------------------------

    if not file or file.filename == "":
        return "Please upload your resume!"

    # -----------------------------------------------------
    # GET FILE NAME
    # -----------------------------------------------------

    filename = os.path.basename(
        file.filename
    )

    # -----------------------------------------------------
    # VALIDATE FILE TYPE
    # -----------------------------------------------------

    extension = os.path.splitext(
        filename
    )[1].lower()

    if extension not in [".pdf", ".docx"]:
        return "Only PDF and DOCX files are supported!"

    # =====================================================
    # CREATE TEMPORARY FOLDER
    # =====================================================

    temp_folder = tempfile.mkdtemp(
        prefix="ats_check_"
    )

    try:

        # -------------------------------------------------
        # SAVE CURRENT RESUME
        # -------------------------------------------------

        file_path = os.path.join(
            temp_folder,
            filename
        )

        file.save(
            file_path
        )

        # =================================================
        # EXTRACT RESUME TEXT
        # =================================================

        resume_text = extract_resume(
            file_path
        )

        # =================================================
        # CHECK EXTRACTED TEXT
        # =================================================

        if not resume_text or len(
            resume_text.strip()
        ) < 50:

            return (
                "Could not extract enough text "
                "from this resume. Please upload "
                "a valid PDF or DOCX resume."
            )

        # =================================================
        # ATS ANALYSIS
        # =================================================
        #
        # No Job Description.
        #
        # General ATS score only.
        #
        # =================================================

        ats_result = analyze_ats(
            resume_text
        )

        # =================================================
        # ATS RESULT PAGE
        # =================================================

        return render_template(
            "ats_result.html",
            ats=ats_result,
            resume_name=filename
        )

    finally:

        # -------------------------------------------------
        # DELETE TEMPORARY FOLDER
        # -------------------------------------------------

        shutil.rmtree(
            temp_folder,
            ignore_errors=True
        )


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        debug=True,
        port=5001
    )