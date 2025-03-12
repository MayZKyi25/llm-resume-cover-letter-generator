import os
import sqlite3
import google.generativeai as genai

# Load Google API Key from environment variable
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Google API key is missing! Set it in environment variables.")

# Configure Google AI
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro-latest")  


DB_NAME = "jobs.db"  # Make sure this matches your database name

def get_job_and_user_data(job_id, user_id):
    """Fetch job details and user profile from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    try:
        # Fetch job details
        cursor.execute("SELECT job_title, company_name, location, job_description FROM jobs_listings WHERE job_id = ?", (job_id,))
        job = cursor.fetchone()

        # Fetch user profile
        cursor.execute("SELECT name, email, phone, github, linkedin, projects, classes, other FROM user_info WHERE user_id = ?", (user_id,))
        user = cursor.fetchone()

        if not job:
            raise ValueError(f"No job found with job_id: {job_id}")
        if not user:
            raise ValueError(f"No user found with user_id: {user_id}")

        job_data = {
            "title": job[0],
            "company": job[1],
            "location": job[2],
            "description": job[3]
        }

        user_data = {
            "name": user[0],
            "email": user[1],
            "phone": user[2],
            "github": user[3],
            "linkedin": user[4],
            "projects": user[5],
            "classes": user[6],
            "other_info": user[7]
        }

        return job_data, user_data

    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        conn.close()


def generate_gemini_response(prompt):
    """Generate response from Google Gemini API."""
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        print(f"❌ Gemini API Error: {e}")
        return "Error generating content."


def generate_ai_documents(job_id, user_id):
    """Generate and save AI-generated cover letter and resume."""
    job_data, user_data = get_job_and_user_data(job_id, user_id)

    print(f"🔹 Generating documents for Job: {job_data['title']} | User: {user_data['name']}")

    # **Generate Cover Letter**
    cover_letter_prompt = f"""
    Write a professional cover letter for:
    **{job_data['title']} at {job_data['company']} ({job_data['location']})**
    
    Job Description:
    {job_data['description']}
    
    Candidate Profile:
    - Name: {user_data['name']}
    - Email: {user_data['email']}
    - Phone: {user_data['phone']}
    - GitHub: {user_data['github']}
    - LinkedIn: {user_data['linkedin']}
    - Projects: {user_data['projects']}
    - Classes: {user_data['classes']}
    - Additional Info: {user_data['other_info']}
    
    Format the response in **Markdown**.
    """
    cover_letter = generate_gemini_response(cover_letter_prompt)

    with open("cover_letter.md", "w", encoding="utf-8") as file:
        file.write(cover_letter)

    os.system("pandoc cover_letter.md -o cover_letter.pdf")

    # **Generate Resume**
    resume_prompt = f"""
    Create a professional resume for:
    - Name: {user_data['name']}
    - Email: {user_data['email']}
    - Phone: {user_data['phone']}
    - GitHub: {user_data['github']}
    - LinkedIn: {user_data['linkedin']}
    - Projects: {user_data['projects']}
    - Classes: {user_data['classes']}
    - Additional Info: {user_data['other_info']}
    
    Ensure it aligns with:
    **{job_data['title']} at {job_data['company']} ({job_data['location']})**
    
    Job Description:
    {job_data['description']}
    
    Format the response in **Markdown**.
    """
    resume = generate_gemini_response(resume_prompt)

    with open("resume.md", "w", encoding="utf-8") as file:
        file.write(resume)

    os.system("pandoc resume.md -o resume.pdf")

    print("Documents generated: cover_letter.pdf, resume.pdf")


if __name__ == "__main__":
    # **Hardcoded Job ID & User ID for Testing**
    test_job_id = "E9NcqHJvfLKXQyonAAAAAA=="  
    test_user_id = "2"  

    print(f"Generating documents for Job ID: {test_job_id}, User ID: {test_user_id}")
    generate_ai_documents(test_job_id, test_user_id)
