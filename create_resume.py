import os
import google.generativeai as genai

API_KEY = input("Enter API Key: ")
if not API_KEY:
    raise ValueError("API Key not found.")
print ("\nAPI Key is successfully entered.")

# Configure API Client
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Build prompt with the following inputs: job descripion, personal info, prompt
job_description = """
We are looking for a skilled software engineer with expertise in Python, machine learning, and cloud platforms. The ideal candidate should have at least 2 years of experience working with large datasets and building scalable applications.
"""

personal_info = """
Name: May K.
Skills: Python, Machine Learning, Data Analysis, Cloud Platforms
Education: B.S. in Computer Science (Expected Graduation: May 2025)
Experience: 1-year internship in AI Research with Breath Through Tech AI 
"""

prompt = f"""
Job Description: {job_description}
Personal Information: {personal_info}

Generate a resume in markdown format based on the above information, tailored to the job description.
"""

# Response from the generative model
resume_output = model.generate_content(prompt).text

directory_path = input("\nEnter directory path (e.g., C:/Users/username/Desktop): ")
file_path = os.path.join(directory_path, "resum_template.md")
os.makedirs(os.path.dirname(file_path), exist_ok=True)

# Open the file and write the content
with open(file_path, 'w') as file:
    file.write(resume_output)
print(f"\nResume template is saved to {file_path}")