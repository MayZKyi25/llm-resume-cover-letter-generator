# ************ COMP490Project1MayZKyi_Sprint 4 ************

# File structure overview - COMP490_Project1_Sprint1_MayZK/
## sprint 4 
│── s4_gui.py                          # Sprint 4 GUI (allow user to view job postings, select user to generate llm-created resume & cover letter)
│── s4_generate_resume_with_gemini.py  # AI & Markdown and prompt to generate resume &   coverletter
│── s4_test.py                         # Sprint 4 tests (all in one file)

## sprint 3
│── s3_gui.py                    # Sprint 3 GUI (keep for reference)
│── setup_database.py            # Database setup
│── job_data_handler.py          # Job handling logic
│── s3_test.py    

## sprint 2
│── setup_database.py                     # SQLite database creation
│── job_data_handler.py                   # parsing complicated json data to populate to jobs.db table
│── jobs.db                               # SQLite database for all job postings from two json files

## sprint 1
│── create_resume.py                           

## others
│── main.py                      # Entry point for running the app
│── README.md                    # Instructions to run the project sprints
│── requirements.txt             # Dependencies

# In Sprint 4, 
- User selects a job from the database
- User selects a profile from the database
- Sends data to AI and generates a Markdown Cover Letter & Resume
- Files are saved automatically in pdf format
- Tests

# Setup Instructions

## 0. Clone the Repository
git clone https://github.com/mkyi-bsu/COMP490Project1MayZKyi.git
cd COMP490Project1MayZKyi
## 1. Create and Activate Virtual Environment
python -m venv .venv
source .venv/bin/activate  # For Mac/Linux
# On Windows use: .venv\Scripts\activate
## Install Dependencies
pip install -r requirements.txt
## 1. Setup the Database
python setup_database.py
This populates jobs.db with job listings.

## 2. Run s3_gui.py to enter user info then saved the the entered user data into user_info table under jobs.db
python s3_gui.py
This launches the GUI where users can enter their details and apply for jobs 

## 3. Run python s4_gui.py to selected the job id and user to create LLM-generated cover letter and resume which will be saved to .pdf format using pdflatex
python s4_gui.py
***Note: "Gemini API Error: 429 Resource has been exhausted (e.g. check quota)." could occur when tried to access multiple times. 

# 4.Running Tests
pip install pytest
## Run Tests
pytest s4_test.py
This tests the user data saving function.






# ************ COMP490Project1MayZKyi_Sprint 3 ************

# Interactive Job Selection and User Data Entry
# 1. Overview of Sprint 3
- Sprint 3 introduces an interactive interface that allows users to:

- View job postings stored in the SQLite database (from Sprint 2).
- Select a job from the list to display its full details.
- Input personal details, including:
- Identifying Information: Name, email, phone number, GitHub, LinkedIn, etc and save the entered information to the database in a new user_info table under "job_postings.db"

# 2. Requirements
- Python 3.12 or later
- SQLite3
- pytest (for testing)
- tkinter for GUI
- A virtual environment (recommended)

# 3. Setting Up the Program
# Clone the Repository
    - Clone the repository using the command:git clone <repository_url>
    # Example usage:
    - git clone https://github.com/mkyi-bsu/COMP490Project1MayZKyi.git

# 4. The Interactive Interface
1. First Implementation: (s3_display_all_jobs.py) Console-based
✅ - Displays job all listings from (job_postings.db & job_postings2.db)
✅ - Allows user selection from combined job lists
✅ - Fetches and prints complete job details in the console
✅ - Handles missing databases gracefully
❌ - Not interactive (only console-based, no UI elements)

2. Second Implementation (s3_ui_components) Tkinter-Based UI
✅ - Provides a graphical user interface (GUI) for job selection
✅ - Allows users to enter and save their personal information
✅ - Displays job title, company, location, and description in the UI
❌ - Does not show full job details (full description, missing employment type, date posted, salary, etc.)

# Run the Both Console-based & Tkinter-Based UI
- Run the UI or enter "python3 s3_ui_components.py" in terminal
- A job list will be displayed.
- Selecting a job will show its detailed description.
- For Tkinter-based UI, users can enter personal details and click a "Save" button to store them in the database.

# 5. Database Information
- expands the SQLite database (job_postings.db) by adding a new table for user data.

Database Tables:
- job_postings → Stores job listings.
- user_info (new) → Stores user-entered information.

# 6. Running Automated Tests
pytest s3_test_app.py

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

**** Update: It was fixed. **** 

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





