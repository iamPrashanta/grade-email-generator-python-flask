# Create a test file: test_token.py
import os
from dotenv import load_dotenv

load_dotenv()
token = os.getenv("HF_TOKEN")
print(f"Token exists: {token is not None}")
print(f"Token starts with 'hf_': {token.startswith('hf_') if token else False}")
print(f"Token length: {len(token) if token else 0}")
