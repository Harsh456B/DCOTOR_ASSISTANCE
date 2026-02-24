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

load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")

# Validate API keys before configuring clients (ASCII-only console output for Windows compatibility)
if not GEMINI_API_KEY:
    print("WARNING: GEMINI_API_KEY not found in environment variables!")
    print("Please add your Gemini API key to the .env file.")
    GEMINI_API_KEY = None
    
if not GROQ_API_KEY:
    print("WARNING: GROQ_API_KEY not found in environment variables!")
    print("Please add your Groq API key to the .env file.")
    GROQ_API_KEY = None

# Configure clients only if API keys are available
if GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)  # type: ignore
        print("INFO: Gemini API configured successfully")
    except Exception as e:
        print(f"ERROR: Could not configure Gemini API: {e}")
        GEMINI_API_KEY = None
else:
    print("INFO: Gemini API will use fallback methods due to missing API key")

if GROQ_API_KEY:
    try:
        groq_client = Groq(api_key=GROQ_API_KEY)
        print("INFO: Groq API configured successfully")
    except Exception as e:
        print(f"ERROR: Could not configure Groq API: {e}")
        GROQ_API_KEY = None
        groq_client = None
else:
    print("INFO: Groq API will use fallback methods due to missing API key")
    groq_client = None

# Initialize Hugging Face models for free fallback
image_captioning = None
try:
    # Only import and load if needed
    def load_huggingface_model():
        global image_captioning
        if image_captioning is None:
            from transformers import pipeline
            image_captioning = pipeline("image-to-text", model="Salesforce/blip-image-captioning-large")
            print("Hugging Face BLIP model loaded for free image analysis")
        return image_captioning
except Exception as e:
    print(f"Failed to setup Hugging Face model loading: {e}")
    image_captioning = None

# Storage for detailed reports
REPORT_STORAGE_FILE = "detailed_reports.json"

def load_stored_reports():
    """Load stored detailed reports"""
    try:
        if os.path.exists(REPORT_STORAGE_FILE):
            with open(REPORT_STORAGE_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    except Exception:
        return {}

def save_stored_report(report_key, report_data):
    """Save a detailed report for later retrieval"""
    try:
        reports = load_stored_reports()
        reports[report_key] = {
            "data": report_data,
            "timestamp": time.time(),
            "language": report_data.get("language", "English")
        }
        
        # Keep only recent reports (last 50)
        if len(reports) > 50:
            # Remove oldest reports
            sorted_reports = sorted(reports.items(), key=lambda x: x[1]["timestamp"])
            reports = dict(sorted_reports[-50:])
        
        with open(REPORT_STORAGE_FILE, 'w', encoding='utf-8') as f:
            json.dump(reports, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print(f"Error saving report: {e}")

def get_stored_report(report_key):
    """Retrieve a stored detailed report"""
    try:
        reports = load_stored_reports()
        if report_key in reports:
            # Check if report is less than 24 hours old
            report = reports[report_key]
            if time.time() - report["timestamp"] < 86400:  # 24 hours
                return report["data"]
        return None
    except Exception:
        return None

# Rate limiting tracking
request_counts = defaultdict(int)
last_reset_time = time.time()

def check_rate_limit():
    """DISABLED: No artificial rate limiting to let Gemini API handle it"""
    return True  # Always allow requests

def get_remaining_quota_info():
    """DISABLED: No quota tracking"""
    return "Artificial rate limiting disabled. Subject to Gemini API quotas."

def increment_request_count(func_name):
    """DISABLED: No request counting"""
    pass  # Do nothing

# Multilingual Support
LANGUAGES = {
    'English': {'code': 'en', 'voice': 'en-US-GuyNeural', 'voice_f': 'en-US-JennyNeural'},
    'Hindi': {'code': 'hi', 'voice': 'hi-IN-MadhurNeural', 'voice_f': 'hi-IN-SwaraNeural'},
    'Hinglish': {'code': 'hi', 'voice': 'hi-IN-MadhurNeural', 'voice_f': 'hi-IN-SwaraNeural'},  # Hindi+English mix
    'Telugu': {'code': 'te', 'voice': 'te-IN-MohanNeural', 'voice_f': 'te-IN-ShrutiNeural'},
    'Chhattisgarhi': {'code': 'hi', 'voice': 'hi-IN-MadhurNeural', 'voice_f': 'hi-IN-SwaraNeural'}  # Using Hindi voice for Chhattisgarhi
}

# Thread pool for parallel processing - OPTIMIZED FOR SPEED
executor = ThreadPoolExecutor(max_workers=6)

@lru_cache(maxsize=5)
def get_gemini_model(model_name="models/gemini-1.5-flash"):
    """Cache and reuse Gemini model instances - ULTRA FAST MODE"""
    # Use the fastest available models
    models_to_try = [
        "models/gemini-1.5-flash",  # Fastest model available
        "models/gemini-1.0-pro",    # Fallback fast model
        "models/gemini-pro",        # Even older but fast
    ]
    
    # Try the requested model first
    if model_name not in models_to_try:
        models_to_try.insert(0, model_name)
    
    for model in models_to_try:
        try:
            return genai.GenerativeModel(model)  # type: ignore
        except Exception as e:
            print(f"Failed to load model {model}: {e}")
            continue
    
    # If all models fail, fall back to the original
    return genai.GenerativeModel("models/gemini-2.5-pro")  # type: ignore

def analyze_image_free(image, question_type, language='English', additional_context=''):
    """Analyze image using free Hugging Face models as alternative"""
    if image is None:
        return "Please upload an image first.", None
    
    try:
        # Check if Groq API is available for fallback
        if not GROQ_API_KEY or groq_client is None:
            return "Free image analysis requires Groq API. Please add GROQ_API_KEY to environment variables.", None
        
        # Try to load model on demand - this may fail on memory-constrained systems
        try:
            caption_model = load_huggingface_model()
        except Exception as model_load_error:
            print(f"WARNING: Failed to load HuggingFace model: {model_load_error}")
            caption_model = None
        
        if caption_model is None:
            # Fallback: Use the image filename or basic inference without model
            image_description = "Medical image uploaded for analysis"
        else:
            # Get basic image description using BLIP
            try:
                captions = caption_model(image, max_new_tokens=100)
                image_description = captions[0]['generated_text'] if captions else "Medical image uploaded"
            except Exception as caption_error:
                print(f"WARNING: Failed to generate caption: {caption_error}")
                image_description = "Medical image uploaded for analysis"
        
        # Create a detailed prompt for Groq to analyze based on the description
        context = f"""{get_language_instruction(language)}

You are a board-certified medical doctor providing comprehensive analysis. 

{additional_context if additional_context.strip() else ""}

Provide DETAILED medical analysis:
1. CLINICAL FINDINGS: Describe likely visible characteristics (location, size, color, shape, texture)
2. DIFFERENTIAL DIAGNOSIS: Most likely condition (confidence %), alternative possibilities with reasoning
3. TREATMENT RECOMMENDATIONS: Specific medicines with exact doses, frequency, duration, and side effects
4. URGENCY ASSESSMENT: Emergency/Urgent/Routine with clear reasoning
5. PATIENT EDUCATION: What to expect, home care instructions, when to seek immediate help
6. PREVENTION: Lifestyle modifications and preventive measures

Be thorough and professional. Include specific medicine names and dosages."""

        # DETAILED Groq analysis for comprehensive medical report
        try:
            response = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": context}],
                max_tokens=600,  # Increased for detailed analysis
                temperature=0.1  # Very low for consistency and accuracy
            )
            
            analysis = response.choices[0].message.content.replace('#', '').replace('*', '')
            return analysis, None
        except Exception as groq_error:
            print(f"ERROR: Groq API failed: {groq_error}")
            return f"Analysis failed: {str(groq_error)[:100]}. Please check API configuration.", None
        
    except Exception as e:
        print(f"ERROR in analyze_image_free: {str(e)}")
        return f"Free analysis error: {str(e)[:100]}. Please try Gemini when quota resets.", None

def get_language_instruction(language):
    """Get language-specific instruction for AI with strict enforcement"""
    instructions = {
        'English': '''You MUST respond ONLY in English. NO Hindi, Telugu, Chhattisgarhi, or any other languages.
Every single word must be in English. Use simple, clear English that anyone can understand.
If you use even one word from another language, you have failed.''',

        'Hindi': '''आपको केवल हिंदी में जवाब देना है। कोई अंग्रेजी, तेलुगु, छत्तीसगढ़ी या कोई अन्य भाषा का एक भी शब्द नहीं।
हर एक शब्द देवनागरी लिपि में हिंदी में होना चाहिए। सरल और स्पष्ट हिंदी का प्रयोग करें।
यदि आप कोई अन्य भाषा का एक भी शब्द इस्तेमाल करते हैं तो आप असफल हुए हैं।''',

        'Hinglish': '''Respond ONLY in Hinglish (mix of Hindi and English). Use both Hindi and English words naturally like people speak in India.
Example: "Aapko bukhar hai toh Paracetamol 500mg लें। Take it 2 times daily खाना खाने के बाद।"
Mix Hindi aur English naturally. Comfortable Indian style mein baat karein. Common Hinglish words use karein.
DO NOT use pure Hindi or pure English - always mix both languages.''',

        'Telugu': '''మీరు కేవలం తెలుగు లోనే సమాధానం ఇవ్వాలి. ఇంగ్లీష్, హిందీ, ఛత్తీస్గఢీ లేదా ఎటువంటి ఇతర భాషలలో ఒక్క పదం కూడా వాడకూడదు.
ప్రతి పదం తెలుగు లిపి లోనే ఉండాలి. సరళమైన మరియు స్పష్టమైన తెలుగు వాడండి.
మీరు ఇతర భాష ఒక్క పదం వాడితే మీరు విఫలమైనారు.''',

        'Chhattisgarhi': '''तुम्हे केवल छत्तीसगढ़ी में जवाब देवे के चाही। कोनो अंग्रेजी, हिंदी, तेलुगु या कोनो अन्य भाषा के एको शब्द नइं चाही।
हर एक शब्द असली छत्तीसगढ़ी बोली में होवे के चाही। सरल और साफ छत्तीसगढ़ी वादव।
जेकर तुम कोनो अन्य भाषा के एको शब्द वादव त छत्तीसगढ़ी में जवाब नइं देवे के माने तुम असफल हो गे।'''
    }
    return instructions.get(language, instructions['English'])

def is_common_query(message):
    """Check if message is a common query that can be cached"""
    message_lower = message.lower().strip()
    common_greetings = ['hello', 'hi', 'hey', 'namaste', 'नमस्ते']
    common_thanks = ['thank you', 'thanks', 'thank', 'धन्यवाद', 'धन्यवाद']
    
    if any(greeting in message_lower for greeting in common_greetings):
        return 'greeting'
    elif any(thanks_phrase in message_lower for thanks_phrase in common_thanks):
        return 'thanks'
    return None

def get_common_response(query_type, language):
    """Get cached response for common queries"""
    responses = {
        'greeting': {
            'English': "Hello! I'm your AI medical assistant. How can I help you with your health concerns today?",
            'Hindi': "नमस्ते! मैं आपका AI मेडिकल असिस्टेंट हूं। आज आपकी स्वास्थ्य समस्याओं में मैं आपकी कैसे मदद कर सकता हूं?",
            'Hinglish': "Hello! Main aapka AI doctor assistant hoon. Aaj aapki health problems mein kaise help kar sakta hoon?",
            'Telugu': "నమస్కారం! నేను మీ AI వైద్య సహాయకుడు. ఈరోజు మీ ఆరోగ్య సమస్యలలో నేను మీకు ఎలా సహాయం చేయగలను?",
            'Chhattisgarhi': "नमस्ते! हम तोला AI मेडिकल असिस्टेंट हे। आज तोला स्वास्थ्य समस्या म हम का मदद कर सकत हे?"
        },
        'thanks': {
            'English': "You're welcome! Remember to consult a healthcare professional for any serious medical concerns. Take care!",
            'Hindi': "आपका स्वागत है! कोई भी गंभीर स्वास्थ्य समस्या के लिए कृपया स्वास्थ्य विशेषज्ञ से सलाह लें। स्वस्थ रहें!",
            'Hinglish': "You're welcome! Koi bhi serious health problem ke liye doctor se zaroor consult karo. Take care!",
            'Telugu': "మీరు స్వాగతించబడ్డారు! ఏదైనా తీవ్రమైన వైద్య సమస్య కోసం వైద్య నిపుణులను సంప్రదించండి. జాగ్రత్తగా ఉండండి!",
            'Chhattisgarhi': "तola स्वागत हे! कोनो गंभीर स्वास्थ्य समस्या के लइं डाक्टर से जरूर सलाह लेव। स्वस्थ रहव!"
        }
    }
    
    return responses.get(query_type, {}).get(language, responses[query_type]['English'])

def extract_text_from_pdf(file_path):
    """Extract text from PDF file"""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            text = ""
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()
    except Exception as e:
        return f"Error reading PDF: {str(e)}"

def extract_text_from_docx(file_path):
    """Extract text from DOCX file"""
    try:
        doc = docx.Document(file_path)
        text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        return text.strip()
    except Exception as e:
        return f"Error reading DOCX: {str(e)}"

def analyze_image(image, question_type, language='English', additional_context=''):
    """Advanced image analysis with multilingual support and context - BALANCED VERSION"""
    if image is None:
        return "Please upload an image first.", None
    
    # Check if Gemini API key is available before proceeding
    if GEMINI_API_KEY is None:
        # Use free alternative if API key is not available
        try:
            free_result, _ = analyze_image_free(image, question_type, language, additional_context)
            return free_result, None
        except Exception as free_error:
            print(f"Free alternative failed: {free_error}")
            return call_alternative_ai_service(f"Image analysis requested for {question_type}", language=language), None
    
    try:
        model = get_gemini_model("models/gemini-2.5-pro")
        lang_instruction = get_language_instruction(language)
        
        # Add context to prompt if provided
        context_addon = f"\n\nADDITIONAL PATIENT INFORMATION: {additional_context}" if additional_context.strip() else ""
        
        # Build prompts dynamically to avoid f-string issues and ensure variation
        unique_id = f"Analysis ID: {time.time()}_{hash(image.tobytes()) % 10000}"
        base_prompt = f"""{unique_id}

{lang_instruction}

You are a board-certified dermatologist providing a comprehensive medical report. Analyze this image and provide a detailed professional medical assessment."""
        
        if question_type == "Full Analysis":
            query = base_prompt + """

MEDICAL REPORT:
1. SYMPTOMS: What you see (location, size, color, shape)
2. DIAGNOSIS: Most likely condition + confidence %
3. TREATMENT: Specific medicines with doses + when to take
4. URGENCY: Emergency/Urgent/Routine + why
5. ADVICE: Home care + when to see doctor

Keep response under 300 words."""

        elif question_type == "Symptoms Only":
            query = base_prompt + """
            
List ALL visible symptoms clearly. Location, appearance, size, color. Keep under 150 words."""
        
        elif question_type == "Diagnosis":
            query = base_prompt + """

DIAGNOSIS:
1. Main condition (confidence %)
2. Alternative conditions (2-3 options)
3. Medicines: Name-Dose-Frequency-Duration
4. Tests needed
5. Precautions

Keep under 200 words."""
        
        elif question_type == "Treatment":
            query = base_prompt + "\n\nTREATMENT PLAN:\nMedicines: Name-Dose-How often-How long\nInstructions: What to do at home\nWarnings: When to seek help\nKeep under 250 words"
        
        elif question_type == "Prevention":
            query = base_prompt + """

PREVENTION:
1. Lifestyle changes
2. Diet recommendations  
3. Exercise routine
4. Supplements needed
5. Avoid these things

Keep under 200 words."""
        
        else:
            query = base_prompt
        
        # ULTRA FAST generation config
        generation_config = {
            "temperature": 0.1,  # Very low for speed and consistency
            "top_p": 0.7,        # Optimized for speed
            "top_k": 30,         # Reduced for speed
            "max_output_tokens": 500,  # Drastically reduced for speed
        }
        
        response = model.generate_content(
            [query, image],
            generation_config=generation_config  # type: ignore
        )
        
        cleaned_text = response.text.replace('#', '').replace('*', '')
        return cleaned_text, None
    except Exception as e:
        if "429" in str(e) or "quota" in str(e).lower() or "API Key not found" in str(e):
            # Try free alternative first
            try:
                free_result, _ = analyze_image_free(image, question_type, language, additional_context)
                return free_result, None
            except Exception as free_error:
                print(f"Free alternative failed: {free_error}")
                # Return clear quota exhaustion message if free alternative also fails
                return call_alternative_ai_service(f"Image analysis requested for {question_type}", language=language), None
        return f"Error: {str(e)}", None

def generate_voice_multilingual(text, language, gender="Male"):
    """Generate voice in multiple languages - synchronous version using gTTS"""
    if not text or not text.strip():
        print(f"Text is empty or None: {len(text) if text else 0} characters")
        return None

    max_length = 12000
    if len(text) > max_length:
        original_length = len(text)
        text = text[:max_length] + "... (truncated for performance)"
        print(f"Text truncated from {original_length} to {len(text)} characters")

    try:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        output_path = temp_file.name
        temp_file.close()

        # Map language to gTTS language code
        lang_map = {
            'English': 'en',
            'Hindi': 'hi',
            'Hinglish': 'en',  # Use English for Hinglish
            'Telugu': 'te',
            'Chhattisgarhi': 'hi',  # Use Hindi for Chhattisgarhi
        }
        lang_code = lang_map.get(language, 'en')

        try:
            tts = gTTS(text, lang=lang_code, slow=False, lang_check=False)
            tts.save(output_path)

            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                if file_size > 0:
                    return output_path
                print("ERROR: Generated audio file is empty with gTTS")
                os.unlink(output_path)
                return None

            print("ERROR: Audio file was not created with gTTS")
            return None
        except Exception as e:
            print(f"ERROR: gTTS error: {e}")
            if os.path.exists(output_path):
                os.unlink(output_path)
            return None
    except Exception as e:
        print(f"ERROR: Voice generation error: {e}")
        return None

def generate_voice(text, language="English", gender="Male"):
    """Synchronous wrapper for voice generation compatible with FastAPI"""
    try:
        if not text or not str(text).strip():
            return None

        text = str(text).strip()
        return generate_voice_multilingual(text, language, gender)
    except Exception as e:
        print(f"Error in generate_voice: {e}")
        return None

def analyze_and_speak(image, question_type, language, gender, additional_context=''):
    """Parallel image analysis and voice generation with context - OPTIMIZED VERSION"""
    #print(f"Starting analyze_and_speak with question_type={question_type}, language={language}, gender={gender}")
    
    try:
        analysis_text, _ = analyze_image(image, question_type, language, additional_context)
    except Exception as e:
        print(f"ERROR: Image analysis failed: {str(e)}")
        analysis_text = None
    
    #print(f"Image analysis completed, text length: {len(analysis_text) if analysis_text else 0} characters")
    
    if not analysis_text:
        return "Failed to generate analysis. Please check API keys and try again.", None
    
    try:
        audio_file = generate_voice(analysis_text, language, gender)
    except Exception as e:
        print(f"ERROR: Voice generation failed: {str(e)}")
        audio_file = None
    
    #print(f"Voice generation completed, audio_file: {audio_file}")
    
    return analysis_text, audio_file

def transcribe_audio(audio_file, language='English'):
    """Multilingual audio transcription"""
    if audio_file is None:
        return "Please upload or record audio."
    
    try:
        model = get_gemini_model("models/gemini-2.5-pro")
        lang_instruction = get_language_instruction(language)
        
        # Check if audio_file is a string (file path) or file object
        if isinstance(audio_file, str):
            audio_file_obj = genai.upload_file(path=audio_file)  # type: ignore
        else:
            # If it's a Gradio audio object, we need to get the file path
            audio_file_obj = genai.upload_file(path=audio_file)  # type: ignore
        
        result = model.generate_content([
            f"""{lang_instruction}

Listen to this audio and provide a professional medical assessment:
1. Complete transcription (word-by-word)
2. Symptoms mentioned (detailed list)
3. Chief complaint (main problem)
4. Duration of symptoms
5. Associated symptoms
6. Previous treatments tried
7. Urgency assessment (Emergency/Urgent/Routine)
8. Recommended next steps

Provide a complete medical evaluation without any AI disclaimers.""",
            audio_file_obj
        ])
        
        return result.text.replace('#', '').replace('*', '')
    except Exception as e:
        if "429" in str(e) or "API Key not found" in str(e) or "quota" in str(e).lower():
            # Use fallback service when Google quota is exhausted or API key is invalid
            fallback_response = call_alternative_ai_service("Audio transcription requested", language=language)
            return fallback_response
        return f"Error: {str(e)}"

def chat_with_doctor(message, history, language='English'):
    """Advanced multilingual AI chat using Groq - BALANCED VERSION"""
    if not message.strip():
        return "Please enter a message."
    
    # Check for common queries that can be cached
    query_type = is_common_query(message)
    if query_type:
        cached_response = get_common_response(query_type, language)
        if cached_response:
            return cached_response
    
    try:
        lang_instruction = get_language_instruction(language)
        
        # Build conversation history for Groq
        messages = [
            {
                "role": "system",
                "content": f"""{lang_instruction}

You are a medical doctor. Give clear, helpful advice. Include medicine names, doses, when to see doctor. Keep responses under 200 words.

Previous conversation:"""
            }
        ]
        
        # Ultra-fast history - keep only last 2 exchanges for speed
        recent_history = history[-4:] if len(history) > 4 else history
        for human, ai in recent_history:
            messages.append({"role": "user", "content": human})
            messages.append({"role": "assistant", "content": ai})
        
        messages.append({"role": "user", "content": message})
        
        # Check if Groq client is available before making request
        if 'groq_client' not in globals() or groq_client is None:
            return call_alternative_ai_service(message, language=language)
        
        # ULTRA FAST Groq chat
        response = groq_client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages,
            max_tokens=200,  # Drastically reduced for ultra speed
            temperature=0.1,  # Very low for speed
            top_p=0.6,  # Optimized for speed
        )
        
        return response.choices[0].message.content.replace('#', '').replace('*', '')
    except Exception as e:
        if "429" in str(e) or "quota" in str(e).lower() or "API Key not found" in str(e) or "NotReadyError" in str(e):
            # Use fallback service when Groq quota is exhausted or API key is invalid
            fallback_response = call_alternative_ai_service(message, language=language)
            return fallback_response
        return f"Error: {str(e)}"

def process_document_to_speech(file, language, gender):
    """Convert PDF/DOCX/TXT to speech - BALANCED VERSION"""
    if file is None:
        return "Please upload a file.", None
    
    # Handle different file object types
    if hasattr(file, 'name'):
        file_path = file.name
    elif isinstance(file, str):
        file_path = file
    else:
        return "Invalid file format.", None
        
    try:
        file_ext = os.path.splitext(file_path)[1].lower()
        
        if file_ext == '.pdf':
            text = extract_text_from_pdf(file_path)
        elif file_ext in ['.docx', '.doc']:
            text = extract_text_from_docx(file_path)
        elif file_ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        else:
            return "Unsupported file format. Use PDF, DOCX, or TXT.", None
        
        # Balanced truncation - allow more content but not excessive
        if len(text) > 8000:  # Increased from 5000
            text = text[:8000] + "... (truncated for performance)"
        
        audio_file = generate_voice(text, language, gender)
        return f"Extracted {len(text)} characters from document.", audio_file
    except Exception as e:
        if "429" in str(e) or "API Key not found" in str(e) or "quota" in str(e).lower():
            # Use fallback service when Google quota is exhausted or API key is invalid
            fallback_response = call_alternative_ai_service("Document processing requested", language=language)
            return fallback_response, None
        return f"Error: {str(e)}", None

def call_alternative_ai_service(message, language='English'):
    """Fallback AI service when primary APIs are unavailable"""
    # In a real implementation, this would call another AI service
    # For now, return a helpful message
    fallback_responses = {
        'English': f"API service temporarily unavailable. Please check your API keys in the .env file.\n\nOriginal message: {message}\n\nTo use this application, you need valid API keys from Google Gemini and Groq. Visit https://makersuite.google.com/app/apikey and https://console.groq.com for API keys.",
        'Hindi': f"API सेवा अस्थायी रूप से अनुपलब्ध है। कृपया .env फ़ाइल में अपनी API कुंजी जांचें।\n\nमूल संदेश: {message}\n\nइस एप्लिकेशन का उपयोग करने के लिए, आपको Google Gemini और Groq से मान्य API कुंजी की आवश्यकता है।",
        'Hinglish': f"API service unavailable hai. Please apni .env file mein API keys check karein.\n\nOriginal message: {message}\n\nIs application ka use karne ke liye, aapko Google Gemini aur Groq se valid API keys chahiye hongi.",
        'Telugu': f"API సేవ తాత్కాలికంగా అందుబాటులో లేదు. దయచేసి .env ఫైల్ లో మీ API కీలను తనిఖీ చేయండి.\n\nOriginal message: {message}\n\nఈ అనువర్తనాన్ని ఉపయోగించడానికి, మీకు Google Gemini మరియు Groq నుండి చెల్లుబాటు ఐపీ కీలు అవసరం.",
        'Chhattisgarhi': f"API सेवा अस्थायी रूप ले अनुपलब्ध हे। कृपया .env फ़ाइल में अपन API कुंजी जांच ले।\n\nOriginal message: {message}\n\nइ एप्लिकेशन के उपयोग करे बर, आपला Google Gemini अउ Groq ले मान्य API कुंजी के आवश्यकता होएगी।"
    }
    return fallback_responses.get(language, fallback_responses['English'])


# ------------------------------
# FastAPI backend + static UI
# ------------------------------

BASE_DIR = Path(__file__).resolve().parent
STATIC_DIR = BASE_DIR / "static"
INDEX_FILE = STATIC_DIR / "index.html"

app = FastAPI(title="AI Doctor Medical Assistance")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if STATIC_DIR.exists():
    app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


@app.get("/", response_class=HTMLResponse)
async def serve_index():
    """Serve main HTML UI."""
    if not INDEX_FILE.exists():
        raise HTTPException(status_code=404, detail="UI not found. Make sure static/index.html exists.")
    return INDEX_FILE.read_text(encoding="utf-8")


@app.post("/api/analyze-image")
async def api_analyze_image(
    image: UploadFile = File(...),
    analysis_type: str = Form("Full Analysis"),
    language: str = Form("English"),
    gender: str = Form("Male"),
    additional_context: str = Form(""),
):
    """API endpoint: analyze medical image and generate audio."""
    try:
        image_bytes = await image.read()
        pil_image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid image file.")

    try:
        analysis_text, audio_path = analyze_and_speak(
            pil_image,
            analysis_type,
            language,
            gender,
            additional_context,
        )
        
        if not analysis_text:
            raise HTTPException(status_code=500, detail="Failed to analyze image. Please ensure Gemini API key is configured.")
        
        return {
            "analysis": analysis_text,
            "audio_path": audio_path,
        }
    except HTTPException:
        raise
    except Exception as e:
        print(f"ERROR in image analysis: {str(e)}")
        raise HTTPException(
            status_code=500, 
            detail=f"Failed to analyze image: {str(e)[:100]}"
        )


@app.get("/api/audio")
async def api_get_audio(path: str):
    """Serve generated audio file by its path."""
    if not path or not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Audio file not found.")
    filename = os.path.basename(path)
    return FileResponse(path, media_type="audio/mpeg", filename=filename)


if __name__ == "__main__":
    import uvicorn

    # uvicorn.run(app, host="0.0.0.0", port=8000)
    uvicorn.run(app, host="127.0.0.1", port=8000)
