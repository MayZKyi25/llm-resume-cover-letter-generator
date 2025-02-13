# COMP490Project1MayZKyi_Sprint 1 

# How to Run the Program: Make sure to have the following requriements ready on your device: 
  1. Python 3 installed on your device
  2. A Google AI API Key
  3. The google-generativeai package installed (Install using pip install google-generativeai)

# Running the Program 
  1. Clone the project repository (git clone https://github.com/mkyi-bsu/COMP490Project1MayZKyi.git)
  2. Save the project to your device and open it with a supported IDE
  3. Run the "create_resume.py" script
  4. Enter the Google API key when prompted
  5. Provide a directory path to save the generated resume. The resume will be saved as resume_template.md in the specified directory

# Why I Chose Google Gemini AI
I chose Google’s Gemini AI because it’s free to use and works well for generating structured text like resumes. It understands context, so the resume matches the job description better. It’s also fast and easy to use. Plus, I’m already familiar with Google Cloud, which made it easier to set up.

# The AI Prompt Chosen and Why
I started with a basic prompt, But then I decided to focus more on optimizing the resume for applicant tracking systems (ATS). I modified the prompt to focus on aligning the resume with keywords from the job description to optimize it for applicant tracking systems (ATS). This change made sure the resume would be more likely to pass ATS filters by highlighting key skills and experiences that match the job description.

# COMP490Project1MayZKyi_Sprint 2 
# Sprint2 extracts job postings data from JSON files and inserts it into an SQLite database.

# Requirements 
- Python 3.12 or later
- SQLite3, Pytest, os, time (libraries)
- A virtual environment (not mandatory as long as you have a supported IDE)

# Setting up the Program
1. Clone the Repository
    - git clong <repository_url>
    - cd <repository_folder>
2. Activate Virtual Environment
    - python -m venv venv
    - source venv/bin/activate  # On Windows use: venv\Scripts\activate
3. Run database_sprint2.py file, run the following in terminal or venv
    - python3 database_sprint2.py (database of job posting will be created in the .db format)
4. Verify jobs data insertion to the table, run the followings in terminal or venv
    - sqlite job_postings.db 
    - SELECT COUNT(*) FROM job_postings;
    - to quit control^ + C (on Mac)
5. Run test_database.py 
    - pytest test_database.py





