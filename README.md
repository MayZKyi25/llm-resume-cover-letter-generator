# ************ COMP490Project1MayZKyi_Sprint 1 ************

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

# ************ COMP490Project1MayZKyi_Sprint 2 ************

# Sprint 2 extracts job posting data from JSON files and inserts it into an SQLite database.

# 1. Requirements
    - Python 3.12 or later
    - SQLite3, Pytest, os, time (libraries)
    - A virtual environment (optional, but recommended if you have a supported IDE)
# 2. Setting Up the Program
  # Clone the Repository
    - Clone the repository using the command:git clone <repository_url>
    # Example usage:
    - git clone https://github.com/mkyi-bsu/COMP490Project1MayZKyi.git
  # Navigate into the repository folder:
    - Navigate the repository folder: cd <repository_folder>
    # Example usage: 
    - (Replace <repository_folder> with the folder you used to save the downloaded repository.)
  # Activate the Virtual Environment
    - Create a virtual environment:
    - Enter the command: python -m venv venv
    - source venv/bin/activate # On Windows, use: venv\Scripts\activate

# 3. Running the Python Scripts to See Job Postings Stored in the Database
# 3(a). Run database_sprint2.py

    - Command to run:
    - python3 database_sprint2.py
    - Expected result: A job_posting database will be created in .db format with 1649 rows.
# 3(b). Run handle_rapid_jobs2json.py

    - Command to run:
    - python handle_rapid_jobs2json.py
    - Expected result: A job_posting database will be created in .db format with 386 rows.

# 4. Verify Job Data Insertion into the Table
To verify the job data insertion, run the following commands in the terminal or virtual environment:
    - Open the SQLite database:
    - sqlite3 job_postings.db
    - Example usage: Run the query to count the rows:
    - SELECT COUNT(*) FROM job_postings;

# 5. Run the Tests
    - To run the tests, execute the following command:
    - pytest test_database.py

***** Note: The current version does not correctly handle inserting two types of JSON formats into the same table. To address this, I created the handle_rapid_jobs2json.py script to insert JSON data from rapid_jobs2.json. *****





