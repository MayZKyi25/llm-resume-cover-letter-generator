import os
import pytest
import requests
from unittest.mock import patch
from dotenv import load_dotenv
from s4_generate_resume_with_gemini import generate_ai_documents  

# Load environment variables from .env file 
load_dotenv()

# Sample data
job_data = {
    "title": "Software Engineer",
    "company": "Tech Corp",
    "location": "San Francisco, CA",
    "description": "A dynamic role that involves software development."
}

user_data = {
    "name": "Landon Gray",  
    "email": "landon.gray@example.com",
    "phone": "987-654-3210",
    "github": "github.com/landongray",
    "linkedin": "linkedin.com/in/landongray",
    "projects": "Project A, Project B",  
    "classes": "CS101, CS102",
    "other_info": "Volunteer work at XYZ"
}

# Fetch environment variables (API Key and URL for the LLM API)
API_KEY = os.getenv("GOOGLE_API_KEY")
API_URL = os.getenv("LLM_API_URL")

# 1. Test: Generate AI Documents (Cover Letter and Resume)
@pytest.mark.parametrize("job_id, user_id", [("9ejRCK8AY7OMi9nyAAAAAA==", "3")])
def test_generate_ai_documents(job_id, user_id):
    # Mock the response of generate_gemini_response to simulate API return
    with patch("s4_generate_resume_with_gemini.generate_gemini_response", return_value="Generated cover letter and resume content"):
        # Call the function that generates the documents (cover letter and resume)
        generate_ai_documents(job_id, user_id)

        # Check if both cover letter and resume were generated (you may check for file creation)
        cover_letter_file = f"{user_data['name'].replace(' ', '_')}_cover_letter.pdf"
        resume_file = f"{user_data['name'].replace(' ', '_')}_resume.pdf"

        # Assert that the files were created
        print(f"Cover Letter File: {cover_letter_file}, Resume File: {resume_file}")  # Debugging line
        assert os.path.exists(cover_letter_file), "Cover letter PDF not generated"
        assert os.path.exists(resume_file), "Resume PDF not generated"

# 2. Test: Validate that the prompt includes both job description and user information
@pytest.mark.parametrize("job_id, user_id", [("9ejRCK8AY7OMi9nyAAAAAA==", "3")])
def test_prompt_includes_job_and_user_info(job_id, user_id):
    # Mock job and user data
    mock_job_data = {
        "title": "Software Engineer",
        "company": "Tech Corp",
        "location": "San Francisco, CA",
        "description": "A dynamic role that involves software development."
    }

    mock_user_data = {
        "name": "Landon Gray",  
        
        "email": "landon.gray@example.com",
        "phone": "987-654-3210",
        "github": "github.com/landongray",
        "linkedin": "linkedin.com/in/landongray",
        "projects": "Project A, Project B",  
        
        "classes": "CS101, CS102",
        "other_info": "Volunteer work at XYZ"
    }

    # Mock the function that fetches job and user data
    with patch("s4_generate_resume_with_gemini.get_job_and_user_data", return_value=(mock_job_data, mock_user_data)):
        # Call the function to generate the documents
        generate_ai_documents(job_id, user_id)  

        # Check if both cover letter and resume were generated and contain job and user info
        cover_letter_file = f"{mock_user_data['name'].replace(' ', '_')}_cover_letter.pdf"
        resume_file = f"{mock_user_data['name'].replace(' ', '_')}_resume.pdf"

        # Assert that the files were generated
        print(f"Cover Letter File: {cover_letter_file}, Resume File: {resume_file}")  # Debugging line
        assert os.path.exists(cover_letter_file), "Cover letter PDF not generated"
        assert os.path.exists(resume_file), "Resume PDF not generated"

# 3. Test: Ensure LLM API returns a 200 OK response
@pytest.mark.parametrize("job_id, user_id", [("9ejRCK8AY7OMi9nyAAAAAA==", "3")])
def test_llm_response(job_id, user_id):
    # Prepare the request headers and payload
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {
        "job_id": job_id,
        "user_id": user_id
    }

    # Send a POST request to the API URL
    response = requests.post(API_URL, headers=headers, json=payload)

    # Assert that we get a 200 OK response from the API
    assert response.status_code == 200, f"Expected 200 OK but got {response.status_code}"
