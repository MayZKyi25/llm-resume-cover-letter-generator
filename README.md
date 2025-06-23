# LLM Resume & Cover Letter Generator

This project is an AI-powered application that generates personalized, ATS-optimized resumes and cover letters using Google Gemini AI. Built as my senior capstone at Bridgewater State University, it demonstrates a full-stack development workflow—from data ingestion and database design to LLM prompt engineering and web deployment.

## Project Overview

The tool allows a user to:
1. Select a job posting from a local SQLite database.
2. Enter or select a user profile (name, contact details, GitHub, LinkedIn, projects, coursework).
3. Send both job and profile data to Google Gemini via a structured prompt.
4. Receive back a Markdown-formatted resume and cover letter.
5. Convert those Markdown files to PDF (using pdflatex or a fallback).
6. Save the generated PDFs to disk.

## Features

- End-to-end pipeline for ATS-friendly document creation  
- SQLite database for storing job postings and user profiles  
- Streamlit web interface for interactive selection and data entry  
- Prompt engineering techniques to optimize for keyword matching  
- Markdown-to-PDF conversion for professional formatting  
- Automated tests for core functionality  

## File Structure

llm-resume-cover-letter-generator/
├── sprint1/
│ └── create_resume.py
├── sprint2/
│ ├── setup_database.py
│ └── job_data_handler.py
├── sprint3/
│ ├── s3_gui.py
│ └── s3_test.py
├── sprint4/
│ ├── s4_gui.py
│ ├── s4_generate_resume_with_gemini.py
│ └── s4_test.py
├── jobs.db
├── main.py
├── requirements.txt
├── README.md
└── LICENSE


## Getting Started

1. **Clone the repository**  
   git clone https://github.com/mkyi-bsu/llm-resume-cover-letter-generator.git
   cd llm-resume-cover-letter-generator
   
2. **Create and activate a virtual environment**
    python -m venv .venv
    source .venv/bin/activate      # macOS/Linux
    .venv\Scripts\activate         # Windows

3. **Install dependencies**
   pip install -r requirements.txt

4. **Initialize the database**
   python sprint2/setup_database.py
 
5. **Launch the Streamlit app**
   streamlit run sprint4/s4_gui.py

6. **Running Tests**
   pytest sprint4/s4_test.py
   - Follow the on-screen prompts to select a job and profile, then generate and download your resume and cover letter.
   - If you encounter “429 Resource has been exhausted,” check your Gemini API quota, wait a few minutes, and retry.


## LLM Prompt Strategy

The prompt instructs Gemini to:  
- Draft a concise, ATS-friendly resume tailored to the selected job description.  
- Emphasize keywords and skills that match the job requirements.  
- Format output in Markdown with clear headings and bullet points.  
- Compose a cover letter that addresses the hiring manager, highlights fit, and mirrors the job language.  

## Why Google Gemini AI

Google Gemini AI was chosen because:  
- It excels at structured text generation, producing coherent Markdown.  
- Its strong contextual understanding aligns content precisely with job requirements.  
- The `google-generativeai` package simplifies integration and authentication with Google Cloud.  

## Future Improvements

- Add user authentication and profile management.  
- Implement an ATS-compliance scoring metric.  
- Modularize prompt templates for reuse across document types.  
- Support multiple languages and regional job formats.  
- Deploy as a serverless application (AWS Lambda, Google Cloud Run).  

## License

This project is licensed under the MIT License.  

## Author

May Zar Kyi  
Bridgewater State University
GitHub: https://github.com/mkyi-bsu/resume-generator-gemini-ai  
