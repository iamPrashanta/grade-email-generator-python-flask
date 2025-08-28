import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure Google Generative AI client with your API key
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))

# Create a generative model instance for Gemini 1.5 flash
model = genai.GenerativeModel('gemini-1.5-flash')

prompt_text = "Write a short poem about a rainy day."

try:
    # Generate content from Gemini model
    response = model.generate_content(prompt_text)
    print("Generated Text:\n", response.text)
except Exception as e:
    print(f"An error occurred: {e}")
