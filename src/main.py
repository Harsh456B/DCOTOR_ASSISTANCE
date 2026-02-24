"""
FastAPI main application for Render deployment
"""
import os
from pathlib import Path
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import asyncio
import tempfile
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor
import PyPDF2
import docx
import io
from gtts import gTTS
import time
from collections import defaultdict
import requests
import json
from groq import Groq

from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Validate API keys
if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY not found in environment variables!")
    GEMINI_API_KEY = None
    
if not GROQ_API_KEY:
    print("WARNING: GROQ_API_KEY not found in environment variables!")
    GROQ_API_KEY = None

# Configure clients only if API keys are available
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        print("INFO: Gemini API configured successfully")
    except Exception as e:
        print(f"ERROR: Could not configure Gemini API: {e}")
        GEMINI_API_KEY = None
else:
    print("INFO: Gemini API will use fallback methods due to missing API key")

if GROQ_API_KEY:
    try:
        client = Groq(api_key=GROQ_API_KEY)
        print("INFO: Groq API configured successfully")
    except Exception as e:
        print(f"ERROR: Could not configure Groq API: {e}")
        GROQ_API_KEY = None
else:
    print("INFO: Groq API will use fallback methods due to missing API key")

# Create FastAPI app
app = FastAPI(title="AI Doctor Medical Assistance")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

@app.get("/", response_class=HTMLResponse)
async def serve_index():
    """Serve main HTML UI."""
    INDEX_FILE = STATIC_DIR / "index.html"
    if not INDEX_FILE.exists():
        raise HTTPException(status_code=404, detail="UI not found. Make sure static/index.html exists.")
    return INDEX_FILE.read_text(encoding="utf-8")

@app.get("/health")
async def health_check():
    """Health check endpoint for Render"""
    return {"status": "healthy", "message": "AI Doctor Medical Assistance is running"}

@app.get("/api/status")
async def api_status():
    """API status endpoint"""
    return {
        "status": "online",
        "gemini_api": "available" if GEMINI_API_KEY else "unavailable",
        "groq_api": "available" if GROQ_API_KEY else "unavailable"
    }

# Add your existing API endpoints here
# (I'll include the core functionality from gradio_app_advanced.py)

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)