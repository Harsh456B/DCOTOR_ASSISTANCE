# ADVANCED MEDICAL IMAGE ANALYSIS SYSTEM
# Supports: Multiple languages, Comprehensive analysis, Professional medical advice

import os
from dotenv import load_dotenv
import google.generativeai as genai  # type: ignore
from PIL import Image  # type: ignore

load_dotenv()
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)  # type: ignore

def analyze_medical_image_advanced(image_path, language='English', analysis_depth='comprehensive'):
    """
    Advanced multilingual medical image analysis
    
    Args:
        image_path: Path to medical image file
        language: 'English', 'Hindi', 'Telugu', or 'Chhattisgarhi'
        analysis_depth: 'quick', 'standard', or 'comprehensive'
    
    Returns:
        Detailed medical analysis string
    """
    
    try:
        image = Image.open(image_path)
        model = genai.GenerativeModel('gemini-flash-lite-latest')  # type: ignore
        
        # Language instructions
        lang_map = {
            'English': 'Respond in simple, clear English',
            'Hindi': 'हिंदी में सरल भाषा में जवाब दें',
            'Telugu': 'తెలుగులో సరళంగా సమాధానం ఇవ్వండి',
            'Chhattisgarhi': 'छत्तीसगढ़ी/हिंदी में सरल जवाब दें'
        }
        
        lang_inst = lang_map.get(language, lang_map['English'])
        
        # Comprehensive prompt
        if analysis_depth == 'comprehensive':
            query = f"""{lang_inst}

COMPREHENSIVE MEDICAL IMAGE ANALYSIS:

1. VISUAL EXAMINATION:
   - Detailed description of findings
   - Anatomical areas affected
   - Severity assessment

2. DIFFERENTIAL DIAGNOSIS:
   - Primary diagnosis (most likely)
   - Alternative diagnoses (2-3 options)
   - Reasoning for each

3. COMPLETE PRESCRIPTION:
   Medicine 1: [Name (Brand)] - Dose - Frequency - Timing - Duration
   Medicine 2: [Same format]
   Medicine 3: [Same format]

4. HOME CARE INSTRUCTIONS:
   - Immediate steps
   - Daily routine
   - Diet advice

5. INVESTIGATIONS NEEDED:
   - Lab tests
   - Imaging studies

6. URGENCY ASSESSMENT:
   - Emergency/Urgent/Routine
   - Red flag symptoms

7. FOLLOW-UP:
   - Review timeline
   - Warning signs

Provide detailed professional advice in simple language.
⚠️ Consult licensed doctor for prescription.
"""
        elif analysis_depth == 'standard':
            query = f"""{lang_inst}

1. Symptoms visible
2. Likely condition  
3. Medicines recommended (name, dose, frequency)
4. Home care
5. When to see doctor
6. Precautions
"""
        else:  # quick
            query = f"""{lang_inst}

Quick analysis: symptoms, condition, basic treatment, urgency.
"""
        
        response = model.generate_content(
            [query, image],
            generation_config={  # type: ignore
                "temperature": 0.5,
                "top_p": 0.85,
                "max_output_tokens": 2048,
            }
        )
        
        # Clean output
        result = response.text.replace('#', '').replace('*', '')
        return result
        
    except Exception as e:
        return f"Error: {str(e)}"

# Main execution
if __name__ == "__main__":
    image_path = "images.jpeg"
    
    print("=" * 80)
    print("ADVANCED MEDICAL IMAGE ANALYSIS SYSTEM")
    print("=" * 80)
    
    # Comprehensive analysis in English
    print("\n[COMPREHENSIVE ANALYSIS - ENGLISH]\n")
    result = analyze_medical_image_advanced(image_path, language='English', analysis_depth='comprehensive')
    print(result)
    
    # Hindi analysis
    print("\n" + "=" * 80)
    print("\n[STANDARD ANALYSIS - HINDI]\n")
    result_hindi = analyze_medical_image_advanced(image_path, language='Hindi', analysis_depth='standard')
    print(result_hindi)