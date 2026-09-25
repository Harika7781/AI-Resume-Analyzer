
import os
import json
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google import genai
from PyPDF2 import PdfReader


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="ResumeIQ | AI Resume Analyzer",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# ============================================================
# PATHS + ENVIRONMENT
# ============================================================

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

API_KEY = os.getenv("GEMINI_API_KEY")


# ============================================================
# LOAD CSS
# ============================================================

def load_css():
    css_path = BASE_DIR / "style.css"

    if not css_path.exists():
        st.error(
            "style.css was not found. Make sure app.py and "
            "style.css are in the same folder."
        )
        return

    css = css_path.read_text(encoding="utf-8")

    # This is the ONLY HTML in the application.
    # It is used only to load CSS. The visible UI below
    # uses native Streamlit components, so raw <div>/<span>
    # text cannot appear in the interface.
    st.markdown(
        "<style>" + css + "</style>",
        unsafe_allow_html=True,
    )


load_css()


# ============================================================
# GEMINI
# ============================================================

if not API_KEY:
    st.error("GEMINI_API_KEY was not found in your .env file.")
    st.stop()


@st.cache_resource
def get_client():
    return genai.Client(api_key=API_KEY)


client = get_client()


# ============================================================
# SESSION STATE
# ============================================================

if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None


# ============================================================
# HEADER
# ============================================================

header_left, header_right = st.columns([5, 2])

with header_left:
    st.markdown("#  ResumeIQ")
    st.caption("AI Resume & Career Intelligence")

with header_right:
    st.success("● Gemini AI Connected")


# ============================================================
# HERO
# ============================================================

with st.container(border=True):

    st.markdown("## Make your resume **job-ready.**")

    st.write(
        "Compare your resume with any job description, "
        "discover skill gaps, improve your application, "
        "and prepare for interviews using Generative AI."
    )

    feature1, feature2, feature3, feature4 = st.columns(4)

    with feature1:
        st.info(" **Job Match**\n\nCompare resume and JD.")

    with feature2:
        st.info(" **Skill Gaps**\n\nFind missing requirements.")

    with feature3:
        st.info(" **Improve**\n\nGet actionable suggestions.")

    with feature4:
        st.info(" **Interview**\n\nPrepare role-specific questions.")


# ============================================================
# INPUT SECTION
# ============================================================

st.markdown("## Analyze Your Application")

st.caption(
    "Upload your resume and paste the job description "
    "for the role you are targeting."
)


resume_column, job_column = st.columns(2, gap="large")


# ============================================================
# RESUME INPUT
# ============================================================

with resume_column:

    with st.container(border=True):

        st.markdown("###  Your Resume")

        st.caption(
            "Upload your latest resume as a PDF."
        )

        # EXACTLY ONE FILE UPLOADER
        uploaded_resume = st.file_uploader(
            "Upload Resume",
            type=["pdf"],
            key="resume_uploader",
            label_visibility="collapsed",
        )

        if uploaded_resume is not None:

            try:

                pdf_bytes = uploaded_resume.getvalue()

                if not pdf_bytes.startswith(b"%PDF"):

                    st.session_state.resume_text = ""

                    st.error(
                        "The uploaded file does not appear "
                        "to be a valid PDF."
                    )

                else:

                    reader = PdfReader(uploaded_resume)

                    extracted_text = ""

                    for page in reader.pages:

                        page_text = page.extract_text()

                        if page_text:
                            extracted_text += page_text + "\n"

                    extracted_text = extracted_text.strip()

                    if extracted_text:

                        st.session_state.resume_text = (
                            extracted_text
                        )

                        word_count = len(
                            extracted_text.split()
                        )

                        st.success(
                            f"✓ Resume processed successfully • "
                            f"{word_count:,} words extracted"
                        )

                        with st.expander(
                            "Preview extracted resume"
                        ):

                            st.text_area(
                                "Resume Preview",
                                value=extracted_text[:8000],
                                height=230,
                                label_visibility="collapsed",
                                key="resume_preview",
                            )

                    else:

                        st.session_state.resume_text = ""

                        st.warning(
                            "No readable text was found in this PDF."
                        )

            except Exception as error:

                st.session_state.resume_text = ""

                st.error(
                    f"Could not read PDF: {error}"
                )

        else:

            st.caption(
                "PDF format • Text-based resumes recommended"
            )


# ============================================================
# JOB DESCRIPTION
# ============================================================

with job_column:

    with st.container(border=True):

        st.markdown("###  Target Job")

        st.caption(
            "Paste the complete job description."
        )

        job_description = st.text_area(
            "Job Description",
            height=280,
            placeholder=(
                "Paste the complete job description here...\n\n"
                "Example:\n"
                "• Required skills\n"
                "• Responsibilities\n"
                "• Qualifications\n"
                "• Experience\n"
                "• Preferred technologies"
            ),
            key="job_description_input",
            label_visibility="collapsed",
        )

        if job_description.strip():

            word_count = len(
                job_description.split()
            )

            character_count = len(
                job_description
            )

            st.success(
                f"✓ Job description ready • "
                f"{word_count:,} words • "
                f"{character_count:,} characters"
            )

        else:

            st.caption(
                "Tip: Paste the complete JD for better matching."
            )


# ============================================================
# READINESS
# ============================================================

st.markdown("### Application Readiness")

resume_ready = bool(
    st.session_state.resume_text.strip()
)

jd_ready = bool(
    job_description.strip()
)

status1, status2, status3 = st.columns(3)

with status1:
    if resume_ready:
        st.success(" Resume uploaded")
    else:
        st.info("○ Resume waiting")

with status2:
    if jd_ready:
        st.success(" Job description added")
    else:
        st.info("○ Job description waiting")

with status3:
    if resume_ready and jd_ready:
        st.success(" Ready for AI analysis")
    else:
        st.info("○ Complete the inputs")


# ============================================================
# ANALYSIS SETTINGS
# ============================================================

st.markdown("### Analysis Settings")

setting1, setting2, setting3 = st.columns(3)

with setting1:

    analysis_mode = st.selectbox(
        "Analysis Focus",
        [
            "Complete Analysis",
            "Skills & Keywords",
            "Resume Improvement",
            "Interview Preparation",
        ],
        key="analysis_mode",
    )

with setting2:

    experience_level = st.selectbox(
        "Experience Level",
        [
            "Fresher / Graduate",
            "0–2 Years",
            "2–5 Years",
            "5+ Years",
        ],
        key="experience_level",
    )

with setting3:

    target_focus = st.selectbox(
        "Primary Target",
        [
            "Overall Job Fit",
            "Technical Fit",
            "ATS Keywords",
            "Interview Readiness",
        ],
        key="target_focus",
    )


# ============================================================
# ANALYZE BUTTON
# ============================================================

st.markdown("---")

analyze = st.button(
    " Analyze My Resume with AI",
    type="primary",
    key="analyze_button",
    use_container_width=True,
    
)


# ============================================================
# AI ANALYSIS
# ============================================================

if analyze:

    if not resume_ready:
        st.warning("Please upload your resume first.")
        st.stop()

    if not jd_ready:
        st.warning("Please paste the job description first.")
        st.stop()

    prompt = f"""
You are an expert AI career assistant specializing in
resume and job-description analysis.

Analyze the candidate's resume against the target job description.

ANALYSIS FOCUS:
{analysis_mode}

EXPERIENCE LEVEL:
{experience_level}

PRIMARY TARGET:
{target_focus}

================ RESUME ================

{st.session_state.resume_text}

================ JOB DESCRIPTION ================

{job_description}

================ OUTPUT ================

Return ONLY valid JSON.

Use exactly this structure:

{{
    "match_percentage": 0,
    "matching_skills": [],
    "missing_skills": [],
    "improvement_suggestions": [],
    "interview_topics": [],
    "interview_questions": []
}}

RULES:

1. match_percentage must be an integer between 0 and 100.
2. It is an AI-generated estimate and NOT an official ATS score.
3. matching_skills should contain important skills demonstrated
   by the resume and relevant to the job description.
4. missing_skills should contain important job requirements
   absent or weakly demonstrated in the resume.
5. improvement_suggestions must be practical and specific.
6. interview_topics must be relevant to the target role.
7. interview_questions must contain exactly 5 questions.
8. Never invent experience, projects, certifications,
   education, technologies, or skills.
9. Do not assume the candidate knows a technology simply
   because it appears in the job description.
10. Ground the analysis only in the supplied resume and JD.
11. Return JSON only.
12. Do not include Markdown code fences.
"""

    with st.spinner(
        " ResumeIQ is analyzing your application..."
    ):

        try:

            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt,
            )

            result_text = response.text.strip()

            if result_text.startswith("```json"):
                result_text = result_text[
                    len("```json"):
                ].strip()

            if result_text.startswith("```"):
                result_text = result_text[3:].strip()

            if result_text.endswith("```"):
                result_text = result_text[:-3].strip()

            result = json.loads(result_text)

            st.session_state.analysis_result = result

            st.success(
                "Analysis completed successfully."
            )

        except json.JSONDecodeError:

            st.error(
                "Gemini returned an unexpected format. "
                "Please click Analyze again."
            )

            st.stop()

        except Exception as error:

            st.error(
                f"AI analysis failed: {error}"
            )

            st.stop()


# ============================================================
# RESULTS
# ============================================================

result = st.session_state.analysis_result

if result:

    st.markdown("---")

    st.markdown("##  Your AI Resume Analysis")

    st.caption(
        "Insights generated from your resume and target job."
    )

    try:
        score = int(
            result.get("match_percentage", 0)
        )
    except Exception:
        score = 0

    score = max(0, min(100, score))

    matching_skills = result.get(
        "matching_skills", []
    )

    missing_skills = result.get(
        "missing_skills", []
    )

    suggestions = result.get(
        "improvement_suggestions", []
    )

    topics = result.get(
        "interview_topics", []
    )

    questions = result.get(
        "interview_questions", []
    )

    if not isinstance(matching_skills, list):
        matching_skills = []

    if not isinstance(missing_skills, list):
        missing_skills = []

    if not isinstance(suggestions, list):
        suggestions = []

    if not isinstance(topics, list):
        topics = []

    if not isinstance(questions, list):
        questions = []


    # ========================================================
    # SCORE
    # ========================================================

    st.markdown("###  Job Match")

    st.progress(
        score / 100,
        text=f"Estimated Resume–Job Match: {score}%"
    )

    st.caption(
        "This is an AI-generated estimate, not an official ATS score."
    )


    metric1, metric2, metric3, metric4 = st.columns(4)

    with metric1:
        st.metric(
            "Resume–JD Match",
            f"{score}%"
        )

    with metric2:
        st.metric(
            "Matching Skills",
            len(matching_skills)
        )

    with metric3:
        st.metric(
            "Skill Gaps",
            len(missing_skills)
        )

    with metric4:
        st.metric(
            "Interview Questions",
            len(questions)
        )


    # ========================================================
    # SKILLS
    # ========================================================

    st.markdown("###  Skills & Keyword Analysis")

    skill_left, skill_right = st.columns(
        2,
        gap="large"
    )

    with skill_left:

        with st.container(border=True):

            st.markdown("####  Matching Skills")

            st.caption(
                "Relevant skills identified in your resume."
            )

            if matching_skills:

                for skill in matching_skills:

                    st.success(
                        f" {skill}"
                    )

            else:

                st.info(
                    "No strong matching skills detected."
                )


    with skill_right:

        with st.container(border=True):

            st.markdown(
                "####  Missing / Weak Skills"
            )

            st.caption(
                "Important requirements not clearly demonstrated."
            )

            if missing_skills:

                for skill in missing_skills:

                    st.warning(
                        f"! {skill}"
                    )

            else:

                st.success(
                    "No major skill gaps detected."
                )


    # ========================================================
    # IMPROVEMENT PLAN
    # ========================================================

    st.markdown("###  Resume Improvement Plan")

    if suggestions:

        for index, suggestion in enumerate(
            suggestions,
            start=1
        ):

            with st.container(border=True):

                st.markdown(
                    f"**{index}.** {suggestion}"
                )

    else:

        st.info(
            "No improvement suggestions were generated."
        )


    # ========================================================
    # INTERVIEW
    # ========================================================

    st.markdown("###  Interview Preparation")

    topic_column, question_column = st.columns(
        2,
        gap="large"
    )

    with topic_column:

        with st.container(border=True):

            st.markdown(
                "####  Recommended Topics"
            )

            if topics:

                for topic in topics:

                    st.info(
                        f" {topic}"
                    )

            else:

                st.info(
                    "No interview topics generated."
                )


    with question_column:

        with st.container(border=True):

            st.markdown(
                "####  Potential Interview Questions"
            )

            if questions:

                for index, question in enumerate(
                    questions,
                    start=1
                ):

                    with st.expander(
                        f"{index}. {question}"
                    ):

                        st.write(
                            "Prepare your answer using "
                            "your actual projects, skills, "
                            "and experience."
                        )

            else:

                st.info(
                    "No interview questions generated."
                )


    # ========================================================
    # EXPORT
    # ========================================================

    st.markdown("###  Export Analysis")

    analysis_json = json.dumps(
        result,
        indent=4,
        ensure_ascii=False,
    )

    st.download_button(
        label=" Download Complete Analysis",
        data=analysis_json,
        file_name="resumeiq_analysis.json",
        mime="application/json",
        key="download_analysis",
        use_container_width=True,
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "ResumeIQ • AI Resume Analysis • Job Matching • "
    "Skill Gap Detection • Interview Preparation"
)
