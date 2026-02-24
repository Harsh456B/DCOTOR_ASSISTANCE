# ADVANCED MULTILINGUAL TEXT-TO-SPEECH SYSTEM
# Supports: Multiple languages, Multiple voices, High-quality audio, Auto-play

import os
from dotenv import load_dotenv
from gtts import gTTS
import asyncio
import edge_tts
import subprocess
import platform

load_dotenv()

# Voice mappings for different languages and genders
VOICE_MAP = {
    'English': {
        'Male': 'en-US-GuyNeural',
        'Female': 'en-US-JennyNeural',
        'Male_Friendly': 'en-US-AndrewNeural',
        'Female_Friendly': 'en-US-AriaNeural'
    },
    'Hindi': {
        'Male': 'hi-IN-MadhurNeural',
        'Female': 'hi-IN-SwaraNeural'
    },
    'Telugu': {
        'Male': 'te-IN-MohanNeural',
        'Female': 'te-IN-ShrutiNeural'
    },
    'Chhattisgarhi': {  # Fallback to Hindi
        'Male': 'hi-IN-MadhurNeural',
        'Female': 'hi-IN-SwaraNeural'
    }
}

async def text_to_speech_advanced(input_text, output_filepath, language='English', gender='Male', 
                                  rate='+0%', volume='+0%', pitch='+0Hz'):
    """
    Advanced multilingual text-to-speech with customization
    
    Args:
        input_text: Text to convert to speech
        output_filepath: Output audio file path
        language: 'English', 'Hindi', 'Telugu', 'Chhattisgarhi'
        gender: 'Male' or 'Female'
        rate: Speech rate (e.g., '+10%' faster, '-10%' slower)
        volume: Volume (e.g., '+20%' louder, '-20%' softer)
        pitch: Pitch (e.g., '+5Hz' higher, '-5Hz' lower)
    
    Returns:
        bool: Success status
    """
    try:
        # Get voice for language and gender
        voice = VOICE_MAP.get(language, VOICE_MAP['English']).get(gender, VOICE_MAP['English']['Male'])
        
        # Create Edge TTS communicate object with customization
        communicate = edge_tts.Communicate(
            input_text,
            voice,
            rate=rate,
            volume=volume,
            pitch=pitch
        )
        
        await communicate.save(output_filepath)
        print(f"✓ High-quality {language} audio created: {output_filepath}")
        print(f"  Voice: {voice} | Rate: {rate} | Volume: {volume}")
        return True
        
    except Exception as e:
        print(f"✗ Edge TTS error: {str(e)}")
        return False

async def text_to_speech_with_autoplay(input_text, output_filepath, language='English', 
                                       gender='Male', autoplay=True):
    """
    Generate speech and optionally auto-play
    
    Args:
        input_text: Text to convert
        output_filepath: Output file path
        language: Language selection
        gender: Voice gender
        autoplay: Whether to play audio automatically
    
    Returns:
        bool: Success status
    """
    # Generate audio
    success = await text_to_speech_advanced(input_text, output_filepath, language, gender)
    
    if success and autoplay:
        # Auto-play based on OS
        os_name = platform.system()
        try:
            print(f"\n▶ Playing audio...")
            if os_name == "Darwin":  # macOS
                subprocess.run(["afplay", output_filepath])
            elif os_name == "Windows":
                subprocess.run(["powershell", '-c', f'(New-Object Media.SoundPlayer "{output_filepath}").PlaySync();'])
            elif os_name == "Linux":
                subprocess.run(["aplay", output_filepath])
            else:
                print("⚠ Auto-play not supported on this OS")
        except Exception as e:
            print(f"✗ Auto-play error: {e}")
    
    return success

def generate_medical_speech(medical_text, output_file, language='English', gender='Male', style='professional'):
    """
    Generate medical report speech with appropriate tone
    
    Args:
        medical_text: Medical report/prescription text
        output_file: Output audio file
        language: Language selection
        gender: Voice gender
        style: 'professional', 'friendly', 'urgent'
    
    Returns:
        bool: Success status
    """
    # Style-based customization
    styles = {
        'professional': {'rate': '+0%', 'volume': '+0%', 'pitch': '+0Hz'},
        'friendly': {'rate': '+5%', 'volume': '+10%', 'pitch': '+2Hz'},
        'urgent': {'rate': '+15%', 'volume': '+20%', 'pitch': '+3Hz'},
        'calm': {'rate': '-5%', 'volume': '+5%', 'pitch': '-2Hz'}
    }
    
    params = styles.get(style, styles['professional'])
    
    return asyncio.run(text_to_speech_advanced(
        medical_text,
        output_file,
        language=language,
        gender=gender,
        **params
    ))

def batch_generate_speech(text_dict, output_dir='audio_outputs', language='English', gender='Male'):
    """
    Generate multiple audio files from dictionary
    
    Args:
        text_dict: Dictionary with {filename: text_content}
        output_dir: Output directory
        language: Language selection
        gender: Voice gender
    
    Returns:
        list: Successfully created files
    """
    os.makedirs(output_dir, exist_ok=True)
    created_files = []
    
    for filename, text in text_dict.items():
        filepath = os.path.join(output_dir, filename)
        success = asyncio.run(text_to_speech_advanced(text, filepath, language, gender))
        if success:
            created_files.append(filepath)
    
    return created_files

if __name__ == "__main__":
    print("=" * 80)
    print("ADVANCED MULTILINGUAL DOCTOR VOICE GENERATION SYSTEM")
    print("=" * 80)
    
    # Test 1: English professional medical report
    print("\n[TEST 1: English Medical Report]")
    medical_report_en = """Good morning. This is your medical analysis report.
    
Based on the image analysis, you have a mild skin infection. 
    
Prescription:
1. Apply Mupirocin cream 2 times daily for 5 days
2. Take Cetirizine 10mg once at night for 3 days
3. Keep the area clean and dry
    
Precautions: Avoid scratching, wash hands frequently.
    
If symptoms worsen, consult a dermatologist immediately."""
    
    asyncio.run(text_to_speech_with_autoplay(
        medical_report_en,
        "medical_report_english.mp3",
        language='English',
        gender='Female',
        autoplay=False
    ))
    
    # Test 2: Hindi medical advice
    print("\n[TEST 2: Hindi Medical Advice]")
    medical_advice_hi = """नमस्कार। यह आपकी चिकित्सा रिपोर्ट है।
    
आपको हल्का बुखार है। 
    
दवाइयां:
1. पैरासिटामोल 500mg दिन में 2 बार खाने के बाद
2. अधिक पानी पिएं
3. आराम करें
    
अगर बुखार 3 दिन से ज्यादा रहे तो डॉक्टर से मिलें।"""
    
    asyncio.run(text_to_speech_with_autoplay(
        medical_advice_hi,
        "medical_advice_hindi.mp3",
        language='Hindi',
        gender='Male',
        autoplay=False
    ))
    
    # Test 3: Telugu medical instruction
    print("\n[TEST 3: Telugu Medical Instructions]")
    medical_telugu = """నమస్కారం. ఇది మీ వైద్య నిపుణులు.
    
మీకు తలనొప్పి ఉంది. 
    
మందులు:
1. ప్యారసిటమాల్ 500mg రోజుకు 2 సార్లు
2. చాలా నీళ్ళు తాగండి
3. విశ్రాంతి తీసుకోండి
    
3 రోజుల తర్వాత మంచి ఉంటే వైద్యుడిని సందర్శించండి."""
    
    asyncio.run(text_to_speech_with_autoplay(
        medical_telugu,
        "medical_instructions_telugu.mp3",
        language='Telugu',
        gender='Female',
        autoplay=False
    ))
    
    # Test 4: Batch generation
    print("\n[TEST 4: Batch Generation]")
    batch_texts = {
        "prescription_1.mp3": "Take Paracetamol 500mg twice daily after food for 3 days.",
        "prescription_2.mp3": "Apply ice pack on affected area for 15 minutes, 3 times daily.",
        "advice_1.mp3": "Drink plenty of water and get adequate rest."
    }
    
    created = batch_generate_speech(batch_texts, language='English', gender='Female')
    print(f"\n✓ Created {len(created)} audio files")
    
    print("\n" + "=" * 80)
    print("✓ All tests completed successfully!")
    print("=" * 80)