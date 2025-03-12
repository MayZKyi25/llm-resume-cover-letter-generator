import google.generativeai as genai
import os

# Load API key from environment variable
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("Google API key is missing!")

# Configure Google Gemini AI
genai.configure(api_key=GOOGLE_API_KEY)

# List available models
available_models = genai.list_models()
for model in available_models:
    print(model.name)
