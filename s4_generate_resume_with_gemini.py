import os
import sqlite3
import google.generativeai as genai
import shutil

# Load Google API Key from environment variable
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Google API key is missing! Set it in environment variables.")

# Configure Google AI
genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro-latest")

DB_NAME = "jobs.db"  # Ensure this matches your database name

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
            print(f"No job found with job_id: {job_id}")
            return None, None
        if not user:
            print(f"No user found with user_id: {user_id}")
            return None, None

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
        return None, None
    finally:
        conn.close()

def generate_gemini_response(prompt):
    """Generate response from Google Gemini API."""
    try:
        response = model.generate_content(prompt)
        return response.text if response.text else "No response generated."
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return ""  # Return empty string to avoid writing errors in documents

def check_pdflatex():
    """Check if pdflatex is installed."""
    return shutil.which("pdflatex") is not None

def save_markdown_to_pdf(markdown_text, output_filename):
    """Save Markdown file, convert to LaTeX, and generate a PDF using pdflatex."""
    md_filename = output_filename + ".md"
    tex_filename = output_filename + ".tex"
    pdf_filename = output_filename + ".pdf"

    # Save Markdown content
    with open(md_filename, "w", encoding="utf-8") as file:
        file.write(markdown_text)

    # Convert Markdown to LaTeX using Pandoc
    if shutil.which("pandoc"):
        os.system(f"pandoc {md_filename} -s -o {tex_filename}")
    else:
        print("❗ Pandoc is not installed! Install it before converting Markdown to LaTeX.")
        return

    # Use pdflatex to generate PDF
    if check_pdflatex():
        os.system(f"pdflatex -interaction=nonstopmode {tex_filename}")
        if os.path.exists("texput.pdf"):
            os.rename("texput.pdf", pdf_filename)
    else:
        print("❗ pdflatex is not installed! Install it before converting LaTeX to PDF.")

def generate_ai_documents(job_id, user_id):
    """Generate and save AI-generated cover letter and resume."""
    job_data, user_data = get_job_and_user_data(job_id, user_id)

    if not job_data or not user_data:
        print("❗ Could not fetch job or user data. Aborting document generation.")
        return

    print(f"📄 Generating documents for Job: {job_data['title']} | User: {user_data['name']}")

    # Sanitize file names
    safe_job_title = job_data['title'].replace(" ", "_").replace("/", "_")
    safe_user_name = user_data['name'].replace(" ", "_")

    # **Generate Cover Letter**
    cover_letter_prompt = f"""
    You are a professional career coach and resume expert. Your task is to generate a highly personalized and compelling cover letter for a job application. 

    ### **Instructions:**
    - Keep the tone professional yet enthusiastic.
    - Align the applicant’s skills and experience with the job description.
    - Make it engaging and avoid generic phrases.
    - Maintain a formal **business letter format** with proper sections.

    ---
    
    ### **🔹 Applicant Information**
    - **Full Name:** {user_data['name']}
    - **Email:** {user_data['email']}
    - **Phone:** {user_data['phone']}
    - **LinkedIn:** {user_data['linkedin']}
    - **GitHub:** {user_data['github']}
    - **Key Projects:** {user_data['projects']}
    - **Relevant Coursework:** {user_data['classes']}
    - **Additional Information:** {user_data['other_info']}

    ---
    
    ### **🔹 Job Information**
    - **Position:** {job_data['title']}
    - **Company:** {job_data['company']}
    - **Location:** {job_data['location']}
    - **Job Description:**  
    {job_data['description']}

    ---
    
    **Cover Letter Format:**
    - **Use a professional tone** but keep it engaging.
    - **Start with a strong opening paragraph** that expresses enthusiasm and interest in the role.
    - **The second paragraph** should align the applicant’s skills and projects with the job requirements.
    - **The third paragraph** should highlight relevant achievements or experiences.
    - **The closing paragraph** should express eagerness to interview and include a polite call to action.

    **Ensure the cover letter follows this format:**
    
    **[Full Name]**  
    [Your Address]  
    [Phone Number]  
    [Email]  
    [LinkedIn]  
    [GitHub]  

    [Date]  

    **Hiring Team**  
    {job_data['company']}  
    {job_data['location']}  

    **Subject:** Application for {job_data['title']} at {job_data['company']}  

    **Dear Hiring Team,**  

    [Opening paragraph - express excitement for the role, mention why this company]  

    [Skills & experience paragraph - align skills & projects with job requirements]  

    [Achievements paragraph - mention a key challenge, solved problem, or unique value]  

    [Closing paragraph - express eagerness for an interview, call to action]  

    **Sincerely,**  
    {user_data['name']}  
    """

    cover_letter = generate_gemini_response(cover_letter_prompt)

    if cover_letter.strip():
        save_markdown_to_pdf(cover_letter, f"{safe_user_name}_cover_letter")
    else:
        print("❗ Cover letter generation failed.")

    # **Generate Resume**
    resume_prompt = f"""
    You are an expert resume writer and career strategist. Your task is to generate a **highly professional, ATS-optimized, and well-structured resume** tailored for the **Software Developer position at Pearson**. The resume must be **concise, engaging, and aligned** with the job description.

    ---

    ### **📌 Instructions**
    - The resume should be **formatted in Markdown**.
    - Use **clear section headings** (`## Summary`, `## Experience`, etc.).
    - Keep the **tone professional, concise, and results-oriented**.
    - Ensure the content is **ATS-friendly** (Applicant Tracking System compliant).
    - Include **bullet points** to highlight key achievements and skills.
    - Use **powerful action verbs** (e.g., "Developed", "Implemented", "Optimized").
    - If experience is missing, focus on **projects** to demonstrate expertise.
    - Ensure **all provided information** is correctly included.

    ---

    ### **🔹 Candidate Profile**
    - **Name:** {user_data['name']}
    - **Email:** {user_data['email']}
    - **Phone:** {user_data['phone']}
    - **LinkedIn:** {user_data['linkedin']}
    - **GitHub:** {user_data['github']}
    - **Key Projects:** {user_data['projects']}
    - **Relevant Coursework:** {user_data['classes']}
    - **Additional Info:** {user_data['other_info']}

    ---

    ### **🔹 Job Information**
    - **Position:** {job_data['title']}
    - **Company:** {job_data['company']}
    - **Location:** {job_data['location']}
    - **Job Description:**  
    {job_data['description']}

    ---

    ### **✍️ Resume Structure**
    Ensure the resume follows this format:

    # [Full Name]  
    📞 [Phone Number] | ✉️ [Email] | 🔗 [GitHub] | 🔗 [LinkedIn]  

    ## **Summary**  
    A concise **2-3 sentence professional summary** that showcases **years of experience, expertise in key technologies (C#, Angular, Azure, Kubernetes), and career goals** related to the Pearson job role.  

    ## **Experience**  
    **[Job Title]** – [Company Name] *(Month/Year – Present)*  
    - **Start each bullet point with a strong action verb** (e.g., Developed, Implemented, Optimized).  
    - Quantify impact wherever possible (e.g., "Optimized system performance by **30%**").  
    - Showcase experience with **C#, Angular, cloud technologies, Agile development**.  

    ## **Projects** *(Only if work experience is missing or for additional achievements)*  
    ### **Project Name (e.g., testp1)**  
    🚀 **Technologies:** [C#, Angular, SQL Server, Azure, Kubernetes]  
    - Describe the project in **one or two concise sentences**.  
    - Highlight its **relevance to Pearson’s Item Assist role**.  
    - Mention measurable impact (e.g., **"Reduced processing time by 40%"**).  

    ## **Education**  
    🎓 **[Degree Title]** – [University Name] *(Graduation Year)*  
    Relevant Courses: Networking, Database Systems, Cloud Computing, Software Engineering  

    ## **Skills**  
    - **Languages:** C#, JavaScript/TypeScript  
    - **Frontend:** Angular, React (if applicable)  
    - **Backend:** .NET, REST APIs, SQL Server  
    - **Cloud & DevOps:** Microsoft Azure, Kubernetes, Docker, CI/CD  
    - **Development Practices:** Agile, Unit Testing, API Development  

    ## **Certifications & Awards** *(if applicable)*  
    🏆 [Certification Name] – [Issuing Organization]  
    🏆 [Hackathon/Competition Recognition]  

    ## **Additional Information** *(Optional)*  
    - Open-source contributor for [relevant technology projects].  
    - Passionate about **building intuitive UI/UX** and **collaborating with cross-functional teams**.  

    ---

    ### **🔹 Additional Notes**
    - **If candidate lacks work experience, emphasize relevant projects instead.**
    - **Use strong, active language to showcase impact and skills.**
    - **Ensure the resume is ATS-friendly and formatted cleanly in Markdown.**
    """


if __name__ == "__main__":
    test_job_id = "E9NcqHJvfLKXQyonAAAAAA=="  
    test_user_id = "2"  

    print(f"Generating documents for Job ID: {test_job_id}, User ID: {test_user_id}")
    generate_ai_documents(test_job_id, test_user_id)
