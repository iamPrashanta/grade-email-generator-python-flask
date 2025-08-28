"""
This script is a quick test to verify that your Google Gemini API key is working.
It sends a simple prompt to the Gemini model and prints the response.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv
load_dotenv()
api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise ValueError("❌ GOOGLE_API_KEY is missing! Please add it to your .env file.")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# Test prompt
prompt_text = "Write a short poem about a rainy day."

print("✅ Testing Gemini API key...\n")
try:
    response = model.generate_content(prompt_text)
    if response and hasattr(response, 'text'):
        print("✅ Gemini API is working!\n")
        print("Generated Response:\n", response.text)
    else:
        print("⚠️ No response text returned from the API.")
except Exception as e:
    print(f"❌ An error occurred while testing the API key:\n{e}")
