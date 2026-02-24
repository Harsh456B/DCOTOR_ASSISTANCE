#!/usr/bin/env python3
"""
Script to list all available Google Gemini models and their capabilities.
This helps us identify valid model names and their supported methods.
"""

import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure the API key
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("Error: GEMINI_API_KEY not found in environment variables")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)

def list_available_models():
    """List all available models and their capabilities"""
    print("Available Google Gemini Models:")
    print("=" * 50)
    
    try:
        for model in genai.list_models():
            print(f"Model Name: {model.name}")
            print(f"  Display Name: {model.display_name}")
            print(f"  Description: {model.description}")
            print(f"  Supported Methods: {', '.join(model.supported_generation_methods) if model.supported_generation_methods else 'None'}")
            print("-" * 30)
    except Exception as e:
        print(f"Error listing models: {e}")

if __name__ == "__main__":
    list_available_models()