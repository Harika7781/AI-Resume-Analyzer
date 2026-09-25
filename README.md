ResumeIQ — AI Resume & Job Description Analyzer

> An AI-powered web application that analyzes a resume against a target job description, identifies skill gaps, provides actionable improvement suggestions, and generates role-specific interview questions.

Live Demo

Live Application:
https://resume-analyzer-jobdescription.streamlit.app/

GitHub Repository:
https://github.com/Harika7781/AI-Resume-Analyzer

---

Overview

ResumeIQ is a Generative AI-powered resume analysis application designed to help candidates understand how well their resume aligns with a specific job description.

Users can upload a PDF resume and paste a target job description. The application extracts the resume content, analyzes it against the job requirements using the Gemini API, and presents structured insights through an interactive Streamlit interface.

The application provides:

- Estimated resume–job match percentage
- Matching skills
- Missing or weakly demonstrated skills
- Resume improvement suggestions
- Role-specific interview topics
- Interview questions for preparation

The match percentage is an **AI-generated estimate and is not an official ATS score**.

---

Features

Resume Upload

- Upload a resume in PDF format
- Extract text automatically using PyPDF2
- Validate the uploaded PDF
- Preview extracted resume content

Job Match Analysis

Generative AI compares the resume with the target job description and generates an estimated match percentage.

Skill Gap Detection

Identifies:

- Skills demonstrated in the resume
- Important skills mentioned in the JD but missing or weakly demonstrated in the resume

Resume Improvement

Provides practical suggestions to improve the resume based on the target role.

Interview Preparation

Generates:

- Relevant interview topics
- Five role-specific interview questions

Custom Analysis Settings

Users can select:

- Analysis Focus
- Experience Level
- Primary Target

 Secure API Key Handling

The Gemini API key is not stored in the source code.

For local development, the application uses:

```text
.env
