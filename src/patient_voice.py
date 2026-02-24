# ADVANCED MULTILINGUAL PATIENT VOICE RECORDING & TRANSCRIPTION
# Supports: Audio recording, Gemini transcription, Multiple languages, Medical analysis

import logging
import speech_recognition as sr 
from pydub import AudioSegment  
from io import BytesIO
import os
from dotenv import load_dotenv
import google.generativeai as genai  # type: ignore

load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)  # type: ignore

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def record_audio_advanced(file_path, timeout=30, phrase_time_limit=60, quality='high'):
    """
    Advanced audio recording with quality options
    
    Args:
        file_path: Path to save audio
        timeout: Wait time for speech start (seconds)
        phrase_time_limit: Max recording duration (seconds)
        quality: 'low' (64k), 'medium' (128k), 'high' (192k), 'ultra' (320k)
    
    Returns:
        bool: Success status
    """
    recognizer = sr.Recognizer()
    
    # Quality settings
    bitrates = {
        'low': '64k',
        'medium': '128k',
        'high': '192k',
        'ultra': '320k'
    }
    bitrate = bitrates.get(quality, '192k')
    
    try:
        with sr.Microphone(sample_rate=48000) as source:
            logging.info("Adjusting for ambient noise (enhanced)...")
            recognizer.adjust_for_ambient_noise(source, duration=2)
            recognizer.energy_threshold = 300  # Optimized for voice
            recognizer.dynamic_energy_threshold = True
            
            logging.info("● Start speaking now... (Medical consultation)")
            logging.info(f"Max recording time: {phrase_time_limit} seconds")

            audio_data = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
            logging.info("✓ Recording complete!")

            # High-quality conversion
            wav_data = audio_data.get_wav_data()  # type: ignore
            audio_segment = AudioSegment.from_wav(BytesIO(wav_data))  # type: ignore
            
            # Enhance audio (normalize volume)
            audio_segment = audio_segment.normalize()  # type: ignore
            
            audio_segment.export(file_path, format="mp3", bitrate=bitrate)  # type: ignore

            logging.info(f"✓ High-quality audio saved to {file_path} ({bitrate} bitrate)")
            return True

    except sr.WaitTimeoutError:
        logging.error("✗ No speech detected. Please try again.")
        return False
    except Exception as e:
        logging.error(f"✗ Error: {e}")
        return False

def transcribe_and_analyze_advanced(audio_file, language='English', include_analysis=True):
    """
    Advanced transcription with medical analysis in multiple languages
    
    Args:
        audio_file: Path to audio file
        language: 'English', 'Hindi', 'Telugu', 'Chhattisgarhi'
        include_analysis: Whether to include medical analysis
    
    Returns:
        str: Transcription with optional medical analysis
    """
    try:
        audio_file_obj = genai.upload_file(path=audio_file)  # type: ignore
        model = genai.GenerativeModel('gemini-flash-lite-latest')  # type: ignore
        
        # Language instructions
        lang_instructions = {
            'English': 'Respond in clear, simple English',
            'Hindi': 'हिंदी में साफ जवाब दें',
            'Telugu': 'స్పష్టమైన తెలుగులో సమాధానం ఇవ్వండి',
            'Chhattisgarhi': 'छत्तीसगढ़ी/हिंदी में जवाब दें'
        }
        
        lang_inst = lang_instructions.get(language, lang_instructions['English'])
        
        if include_analysis:
            prompt = f"""{lang_inst}

Advanced Medical Audio Analysis:

1. COMPLETE TRANSCRIPTION:
   - Word-by-word transcription
   - Speaker identification if multiple

2. SYMPTOM EXTRACTION:
   - List ALL symptoms mentioned
   - Duration of each symptom
   - Severity indicators

3. CHIEF COMPLAINT:
   - Main problem patient is facing
   - How it affects daily life

4. MEDICAL HISTORY MENTIONED:
   - Previous conditions
   - Current medications
   - Allergies

5. URGENCY ASSESSMENT:
   - Emergency/Urgent/Routine/Non-urgent
   - Reasoning for urgency level

6. PRELIMINARY ASSESSMENT:
   - Possible conditions (differential diagnosis)
   - Recommended investigations

7. IMMEDIATE RECOMMENDATIONS:
   - What patient should do now
   - When to seek medical help

8. QUESTIONS TO ASK:
   - Important follow-up questions

Provide detailed, professional analysis.
⚠️ AI analysis only. Consult doctor for diagnosis.
"""
        else:
            prompt = f"""{lang_inst}

Accurate transcription:
1. Complete word-by-word transcription
2. Symptoms mentioned
3. Main complaint
4. Urgency level
"""
        
        result = model.generate_content([prompt, audio_file_obj])  # type: ignore
        
        # Clean output
        return result.text.replace('#', '').replace('*', '')
        
    except Exception as e:
        return f"Transcription error: {str(e)}"

if __name__ == "__main__":
    print("=" * 80)
    print("ADVANCED PATIENT VOICE RECORDING & ANALYSIS SYSTEM")
    print("=" * 80)
    
    audio_file_path = "patient_voice_advanced.mp3"
    
    # Step 1: Record high-quality audio
    print("\n[STEP 1: AUDIO RECORDING]")
    print("Please describe your symptoms in detail...\n")
    
    if record_audio_advanced(file_path=audio_file_path, timeout=30, phrase_time_limit=60, quality='high'):
        
        # Step 2: Advanced transcription with medical analysis
        print("\n[STEP 2: TRANSCRIPTION & MEDICAL ANALYSIS]")
        logging.info("Analyzing audio with AI...")
        
        # Comprehensive analysis in English
        analysis = transcribe_and_analyze_advanced(audio_file_path, language='English', include_analysis=True)
        
        print("\n" + "=" * 80)
        print("MEDICAL ANALYSIS REPORT")
        print("=" * 80)
        print(analysis)
        
        # Also get Hindi transcription
        print("\n" + "=" * 80)
        print("HINDI TRANSCRIPTION")
        print("=" * 80)
        hindi_trans = transcribe_and_analyze_advanced(audio_file_path, language='Hindi', include_analysis=False)
        print(hindi_trans)
        
    else:
        logging.warning("✗ Recording failed. Please try again.")
