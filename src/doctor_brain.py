# step1: setup gemini api key
import os
from dotenv import load_dotenv
load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
# step2: convert image to required format 
import base64
from PIL import Image
import google.generativeai as genai

image_path ="images.jpeg"
image_file = open(image_path, "rb")
encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

# step3: multimodal llm with gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-flash-lite-latest')
query = "What are the symptoms shown in the image?"
image = Image.open(image_path)

response = model.generate_content([query, image])

print(response.text)