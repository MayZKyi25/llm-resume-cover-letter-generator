import os
from dotenv import load_dotenv
import google.generativeai as genai
import time 

# Load .env file and API key
load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")
if not API_KEY:
    raise ValueError("API_KEY not found! Make sure to set it in the .env file.")

print(f"API Key Loaded: {API_KEY[:5]}******")  # Print first 5 chars for security

# Configure API client
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel("gemini")

# Define job description and personal information
job_description = """
We are looking for a skilled software engineer with expertise in Python, machine learning, and cloud platforms. The ideal candidate should have at least 2 years of experience working with large datasets and building scalable applications.
"""

personal_info = """
Name: May K.
Skills: Python, Machine Learning, Data Analysis, Cloud Platforms
Education: B.S. in Computer Science (Expected Graduation: May 2025)
Experience: 1-year internship in AI Research with Breath Through Tech AI 
"""

# the prompt
prompt = f"""
Job Description: {job_description}
Personal Information: {personal_info}

Generate a resume in markdown format based on the above information, tailored to the job description.
"""

# Call the model to generate the resume
response = model.generate_content(prompt)
print("Generated Resume:")
print(response.text)

