import openai
import sqlite3
import os
import pypandoc

# Ensure API key is set in environment variables
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("OpenAI API key is missing. Set it in environment variables.")

# OpenAI client setup
client = openai.OpenAI(api_key=OPENAI_API_KEY)

DB_NAME = "jobs.db"  # Ensure this matches your database


def get_job_and_user_data(job_id, user_id):
    """Fetch job details and user profile from the database."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    # Fetch job details
    cursor.execute("SELECT * FROM jobs_listings WHERE job_id = ?", (job_id,))
    job = cursor.fetchone()

    # Fetch user profile
    cursor.execute("SELECT * FROM user_info WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()

    conn.close()

    if not job:
        raise ValueError(f"No job found with job_id: {job_id}")
    if not user:
        raise ValueError(f"No user found with user_id: {user_id}")

    job_data = {
        "title": job[3],
        "company": job[8],
        "location": job[7],
        "description": job[4]
    }

    user_data = {
        "name": user[1],
        "email": user[2],
        "phone": user[3],
        "github": user[4],
        "linkedin": user[5],
        "projects": user[6],
        "classes": user[7],
        "other_info": user[8]
    }

    return job_data, user_data


def generate_openai_response(prompt):
    """Generate response from OpenAI API using the updated format."""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are an AI assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


def save_as_markdown(filename, content):
    """Save content as a Markdown file."""
    with open(filename, "w", encoding="utf-8") as file:
        file.write(content)


def convert_markdown_to_pdf(md_filename, pdf_filename):
    """Convert Markdown file to PDF using pypandoc."""
    try:
        pypandoc.convert_file(md_filename, 'pdf', outputfile=pdf_filename)
        print(f"✅ {pdf_filename} created successfully!")
    except Exception as e:
        print(f"❌ Error converting {md_filename} to PDF: {e}")


def generate_ai_documents(job_id, user_id):
    """Generate and save AI-generated cover letter and resume for a user and job."""
    job_data, user_data = get_job_and_user_data(job_id, user_id)

    # **Generate Cover Letter**
    cover_letter_prompt = f"""
    Write a professional cover letter for the job:
    **{job_data['title']} at {job_data['company']} ({job_data['location']})**
    
    Job Description:
    {job_data['description']}
    
    Based on this user's profile:
    - Name: {user_data['name']}
    - Email: {user_data['email']}
    - Phone: {user_data['phone']}
    - GitHub: {user_data['github']}
    - LinkedIn: {user_data['linkedin']}
    - Projects: {user_data['projects']}
    - Classes: {user_data['classes']}
    - Additional Info: {user_data['other_info']}
    
    Format the response as **Markdown only**.
    """
    cover_letter = generate_openai_response(cover_letter_prompt)

    # Save Cover Letter as Markdown and convert to PDF
    save_as_markdown("cover_letter.md", cover_letter)
    convert_markdown_to_pdf("cover_letter.md", "cover_letter.pdf")

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
    
    Ensure it aligns with the job:
    **{job_data['title']} at {job_data['company']} ({job_data['location']})**
    
    Job Description:
    {job_data['description']}
    
    Format the response as **Markdown only**.
    """
    resume = generate_openai_response(resume_prompt)

    # Save Resume as Markdown and convert to PDF
    save_as_markdown("resume.md", resume)
    convert_markdown_to_pdf("resume.md", "resume.pdf")

    print("✅ Documents generated successfully: cover_letter.pdf, resume.pdf")


if __name__ == "__main__":
    # Test generation with sample job_id and user_id
    test_job_id = "E9NcqHJvfLKXQyonAAAAAA=="  
    test_user_id = "2"   
    generate_ai_documents(test_job_id, test_user_id)
