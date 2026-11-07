import re


# =========================================================
# CONTACT INFORMATION
# =========================================================

def check_contact_info(text):

    score = 0
    details = {}

    # Email
    if re.search(r'[\w\.-]+@[\w\.-]+\.\w+', text):

        score += 3
        details["Email"] = True

    else:

        details["Email"] = False


    # Phone
    if re.search(r'(\+91[\s-]?)?[6-9]\d{9}', text):

        score += 3
        details["Phone"] = True

    else:

        details["Phone"] = False


    # LinkedIn
    if "linkedin.com" in text.lower():

        score += 2
        details["LinkedIn"] = True

    else:

        details["LinkedIn"] = False


    # GitHub
    if "github.com" in text.lower():

        score += 2
        details["GitHub"] = True

    else:

        details["GitHub"] = False


    return score, details


# =========================================================
# RESUME SECTIONS
# =========================================================

def check_sections(text):

    text = text.lower()


    sections = {

        "Education": [
            "education",
            "academic",
            "qualification"
        ],

        "Skills": [
            "skills",
            "technical skills",
            "technologies"
        ],

        "Experience": [
            "experience",
            "work experience",
            "internship"
        ],

        "Projects": [
            "projects",
            "project"
        ],

        "Certifications": [
            "certification",
            "certifications",
            "certificate"
        ]

    }


    found = {}

    score = 0


    for section, keywords in sections.items():

        found[section] = any(
            keyword in text
            for keyword in keywords
        )


        if found[section]:

            score += 3


    return min(score, 15), found


# =========================================================
# SKILL EXTRACTION
# =========================================================

SKILLS = [

    "python",
    "java",
    "c++",
    "javascript",
    "typescript",

    "html",
    "css",

    "sql",
    "mysql",
    "postgresql",
    "mongodb",

    "flask",
    "django",
    "fastapi",

    "react",
    "node.js",
    "express",

    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",

    "pandas",
    "numpy",
    "matplotlib",

    "scikit-learn",
    "tensorflow",
    "pytorch",

    "git",
    "github",

    "docker",
    "kubernetes",

    "aws",
    "azure",
    "gcp",

    "rest api",

    "nlp",
    "opencv"

]


def extract_skills(text):

    text = text.lower()

    found = []


    for skill in SKILLS:

        if skill.lower() in text:

            found.append(skill)


    return found


def check_skills(text):

    found_skills = extract_skills(text)

    score = min(
        len(found_skills),
        20
    )

    return score, found_skills


# =========================================================
# JOB DESCRIPTION KEYWORD MATCH
# =========================================================

def calculate_keyword_match(
    resume_text,
    job_description
):

    if not job_description:

        return {

            "score": 0,

            "required": [],

            "matched": [],

            "missing": []

        }


    jd_skills = extract_skills(
        job_description
    )

    resume_skills = extract_skills(
        resume_text
    )


    if not jd_skills:

        return {

            "score": 0,

            "required": [],

            "matched": [],

            "missing": []

        }


    matched = [

        skill

        for skill in jd_skills

        if skill in resume_skills

    ]


    missing = [

        skill

        for skill in jd_skills

        if skill not in resume_skills

    ]


    score = round(

        (
            len(matched)
            /
            len(jd_skills)
        )
        * 100

    )


    return {

        "score": score,

        "required": jd_skills,

        "matched": matched,

        "missing": missing

    }


# =========================================================
# EXPERIENCE
# =========================================================

def check_experience(text):

    text = text.lower()


    keywords = [

        "experience",
        "internship",
        "intern",
        "developer",
        "engineer",
        "employment",
        "worked"

    ]


    count = sum(

        keyword in text

        for keyword in keywords

    )


    if count >= 5:

        return 15


    if count >= 3:

        return 12


    if count >= 1:

        return 8


    return 3


# =========================================================
# PROJECTS
# =========================================================

def check_projects(text):

    text = text.lower()


    keywords = [

        "project",
        "developed",
        "implemented",
        "created",
        "built",
        "designed"

    ]


    count = sum(

        keyword in text

        for keyword in keywords

    )


    if count >= 5:

        return 10


    if count >= 3:

        return 8


    if count >= 1:

        return 5


    return 0


# =========================================================
# RESUME QUALITY
# =========================================================

def check_quality(text):

    score = 0

    suggestions = []


    word_count = len(
        text.split()
    )


    # Resume length

    if 300 <= word_count <= 1200:

        score += 3

    else:

        suggestions.append(
            "Keep your resume between 300 and 1200 words."
        )


    # Action words

    action_words = [

        "developed",
        "created",
        "implemented",
        "designed",
        "managed",
        "built",
        "optimized"

    ]


    if any(

        word in text.lower()

        for word in action_words

    ):

        score += 3

    else:

        suggestions.append(
            "Use strong action words in your projects and experience."
        )


    # Measurable achievements

    if re.search(
        r'\b\d+%|\b\d+\+|\b\d+\b',
        text
    ):

        score += 2

    else:

        suggestions.append(
            "Add measurable achievements using numbers or percentages."
        )


    # Bullet points

    if "•" in text or "-" in text:

        score += 2

    else:

        suggestions.append(
            "Use bullet points to improve resume readability."
        )


    return score, suggestions


# =========================================================
# RESUME STRENGTHS
# =========================================================

def generate_strengths(
    contact_details,
    section_details,
    skills_score,
    projects_score,
    section_score,
    experience_score,
    quality_score
):

    strengths = []


    # Strong technical skills

    if skills_score >= 10:

        strengths.append(
            "Strong technical skills"
        )


    # Good projects

    if projects_score >= 8:

        strengths.append(
            "Good project section"
        )


    # Contact information

    if contact_details.get("Email") and \
       contact_details.get("Phone"):

        strengths.append(
            "Contact information complete"
        )


    # LinkedIn + GitHub

    if contact_details.get("LinkedIn") and \
       contact_details.get("GitHub"):

        strengths.append(
            "Professional profiles included"
        )


    # Resume structure

    if section_score >= 12:

        strengths.append(
            "Good resume structure"
        )


    # Experience

    if experience_score >= 12:

        strengths.append(
            "Strong experience section"
        )


    # Quality

    if quality_score >= 8:

        strengths.append(
            "Good resume quality"
        )


    return strengths


# =========================================================
# MAIN ATS ANALYZER
# =========================================================

def analyze_ats(
    text,
    job_description=""
):


    # =====================================================
    # INVALID RESUME
    # =====================================================

    if not text or len(
        text.strip()
    ) < 50:

        return {

            "ats_score": 0,

            "contact_score": 0,

            "section_score": 0,

            "skills_score": 0,

            "experience_score": 0,

            "projects_score": 0,

            "quality_score": 0,

            "skills": [],

            "section_details": {},

            "contact_details": {},

            "strengths": [],

            "keyword_score": 0,

            "required_keywords": [],

            "matched_keywords": [],

            "missing_keywords": [],

            "suggestions": [

                "Unable to analyze the resume."

            ]

        }


    # =====================================================
    # CONTACT
    # =====================================================

    contact_score, contact_details = \
        check_contact_info(text)


    # =====================================================
    # SECTIONS
    # =====================================================

    section_score, section_details = \
        check_sections(text)


    # =====================================================
    # SKILLS
    # =====================================================

    skills_score, found_skills = \
        check_skills(text)


    # =====================================================
    # EXPERIENCE
    # =====================================================

    experience_score = \
        check_experience(text)


    # =====================================================
    # PROJECTS
    # =====================================================

    projects_score = \
        check_projects(text)


    # =====================================================
    # QUALITY
    # =====================================================

    quality_score, suggestions = \
        check_quality(text)


    # =====================================================
    # JOB KEYWORD MATCHING
    # =====================================================

    keyword_result = \
        calculate_keyword_match(
            text,
            job_description
        )


    # =====================================================
    # BASE SCORE
    # =====================================================

    base_score = (

        contact_score
        +
        section_score
        +
        skills_score
        +
        experience_score
        +
        projects_score
        +
        quality_score

    )


    # =====================================================
    # ATS SCORE
    # =====================================================

    if job_description:

        keyword_points = round(

            keyword_result["score"]
            * 0.20

        )


        ats_score = (
            base_score
            +
            keyword_points
        )


    else:

        ats_score = round(

            (
                base_score
                /
                80
            )
            * 100

        )


    # =====================================================
    # ADDITIONAL SUGGESTIONS
    # =====================================================

    if not contact_details["LinkedIn"]:

        suggestions.append(
            "Add your LinkedIn profile."
        )


    if not contact_details["GitHub"]:

        suggestions.append(
            "Add your GitHub profile."
        )


    if not section_details["Certifications"]:

        suggestions.append(
            "Consider adding a Certifications section."
        )


    if len(found_skills) < 5:

        suggestions.append(
            "Add more relevant technical skills."
        )


    if keyword_result["missing"]:

        suggestions.append(
            "Add relevant keywords from the target job description."
        )


    # =====================================================
    # GENERATE RESUME STRENGTHS
    # =====================================================

    strengths = generate_strengths(

        contact_details,

        section_details,

        skills_score,

        projects_score,

        section_score,

        experience_score,

        quality_score

    )


    # =====================================================
    # FINAL RESULT
    # =====================================================

    return {

        "ats_score":
            min(
                ats_score,
                100
            ),


        "contact_score":
            contact_score,


        "section_score":
            section_score,


        "skills_score":
            skills_score,


        "experience_score":
            experience_score,


        "projects_score":
            projects_score,


        "quality_score":
            quality_score,


        "skills":
            found_skills,


        # IMPORTANT:
        # Used by Missing Sections Detector

        "section_details":
            section_details,


        # IMPORTANT:
        # Used by Resume Strengths

        "contact_details":
            contact_details,


        "strengths":
            strengths,


        "keyword_score":
            keyword_result["score"],


        "required_keywords":
            keyword_result["required"],


        "matched_keywords":
            keyword_result["matched"],


        "missing_keywords":
            keyword_result["missing"],


        "suggestions":
            suggestions

    }