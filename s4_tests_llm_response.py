import requests
import os
from dotenv import load_dotenv
import pytest
from s4_generate_resume_with_gemini import generate_ai_documents

# Sample data
job_data = {
    "title": "Software Engineer",
    "company": "Tech Corp",
    "location": "San Francisco, CA",
    "description": "A dynamic role that involves software development."
}

user_data = {
    "name": "Sophia Zhang",
    "email": "sophia@example.com",
    "phone": "123-456-7890",
    "github": "github.com/sophia",
    "linkedin": "linkedin.com/in/sophia"
}

@pytest.mark.parametrize("job_id, user_id", [("9ejRCK8AY7OMi9nyAAAAAA==", "3")])  # Example IDs
def test_prompt_includes_job_and_user_info(job_id, user_id):
    # Generate the prompts (assuming your functions generate cover letter and resume)
    cover_letter_prompt = generate_cover_letter_prompt(job_id, user_id)
    resume_prompt = generate_resume_prompt(job_id, user_id)

    # Assert that the job description is in both prompts
    assert "Job Description:" in cover_letter_prompt, "Job description is missing in the cover letter prompt"
    assert "Job Description:" in resume_prompt, "Job description is missing in the resume prompt"

    # Assert that user information is included in both prompts
    assert user_data["name"] in cover_letter_prompt, "User information is missing in the cover letter prompt"
    assert user_data["name"] in resume_prompt, "User information is missing in the resume prompt"
#=======================================================================================================
import pytest

# Sample job and user data for testing
job_data = {
    "title": "Software Engineer",
    "company": "Tech Corp",
    "location": "San Francisco, CA",
    "description": "A dynamic role that involves software development."
}

user_data = {
    "name": "Sophia Zhang",
    "email": "sophia@example.com",
    "phone": "123-456-7890",
    "github": "github.com/sophia",
    "linkedin": "linkedin.com/in/sophia"
}

@pytest.mark.parametrize("job_id, user_id", [("9ejRCK8AY7OMi9nyAAAAAA==", "3")])  # Example IDs
def test_generate_ai_documents(job_id, user_id):
    # Call the function that generates the documents
    result = generate_ai_documents(job_id, user_id)

    # Check if both cover letter and resume are generated (you may adjust the expected result)
    assert result is not None, "Document generation returned None"
    assert "cover letter" in result.lower(), "Cover letter was not generated"
    assert "resume" in result.lower(), "Resume was not generated"


#=======================================================================================================



# Load environment variables (GitHub Secrets or .env file)
load_dotenv()

# API url
API_URL = os.getenv("LLM_API_URL")

# GitHub secret or .env environment variable
API_KEY = os.getenv("GOOGLE_API_KEY")

@pytest.mark.parametrize("job_id, user_id", [("9ejRCK8AY7OMi9nyAAAAAA==", "3")])  
def test_llm_response(job_id, user_id):
    # Prepare the request headers and payload
    headers = {"Authorization": f"Bearer {API_KEY}"}
    payload = {
        "job_id": job_id,
        "user_id": user_id
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    # Assert that we get a 200 OK response
    assert response.status_code == 200, f"Expected 200 OK but got {response.status_code}"

@pytest.mark.parametrize("job_id, user_id", [("9ejRCK8AY7OMi9nyAAAAAA==", "3")])  # Example IDs
def test_prompt_includes_job_and_user_info(job_id, user_id):
    # Mock the job data
    mock_job_data = {
        "title": "Software Engineer",
        "company": "Tech Corp",
        "location": "San Francisco, CA",
        "description": "A dynamic role that involves software development."
    }

    # Mock the user data
    mock_user_data = {
        "name": "Sophia Zhang",
        "email": "sophia@example.com",
        "phone": "123-456-7890",
        "github": "github.com/sophia",
        "linkedin": "linkedin.com/in/sophia"
    }

    # Mock the function that fetches job and user data
    with patch("your_module.get_job_and_user_data", return_value=(mock_job_data, mock_user_data)):
        
        # Generate the cover letter prompt
        cover_letter_prompt = generate_cover_letter_prompt(job_id, user_id)
        resume_prompt = generate_resume_prompt(job_id, user_id)

        # Assert that the job description is included in the prompt
        assert "Job Description:" in cover_letter_prompt, "Job description missing in cover letter prompt"
        assert "Job Description:" in resume_prompt, "Job description missing in resume prompt"

        # Assert that user information is included
        assert mock_user_data["name"] in cover_letter_prompt, "User information missing in cover letter prompt"
        assert mock_user_data["name"] in resume_prompt, "User information missing in resume prompt"
