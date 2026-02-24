import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import asyncio
from PIL import Image
import numpy as np

# Create a simple test image
def create_test_image():
    """Create a simple test image"""
    # Create a simple grayscale image
    img_array = np.random.randint(0, 255, (100, 100), dtype=np.uint8)
    img = Image.fromarray(img_array, mode='L')
    return img

def test_analyze_and_speak():
    """Test the analyze_and_speak function with a dummy image"""
    try:
        # Import the function
        from gradio_app_advanced import analyze_and_speak
        
        # Create a test image
        test_image = create_test_image()
        
        # Test parameters
        question_type = "Symptoms Only"
        language = "English"
        gender = "Male"
        additional_context = "Patient has fever and headache"
        
        print("Testing analyze_and_speak function...")
        print(f"Question type: {question_type}")
        print(f"Language: {language}")
        print(f"Gender: {gender}")
        print(f"Additional context: {additional_context}")
        
        # Call the function
        analysis_text, audio_file = analyze_and_speak(
            test_image, 
            question_type, 
            language, 
            gender, 
            additional_context
        )
        
        print(f"Analysis text length: {len(analysis_text) if analysis_text else 0} characters")
        print(f"Audio file: {audio_file}")
        
        if analysis_text:
            print("✓ Analysis text generated successfully")
            print(f"First 200 characters: {analysis_text[:200]}...")
        else:
            print("✗ Failed to generate analysis text")
            
        if audio_file:
            print("✓ Audio file generated successfully")
            # Check file size
            file_size = os.path.getsize(audio_file)
            print(f"Audio file size: {file_size} bytes")
            # Clean up
            os.unlink(audio_file)
            print("✓ Cleaned up audio file")
        else:
            print("✗ Failed to generate audio file")
            
        return analysis_text is not None, audio_file is not None
        
    except Exception as e:
        print(f"✗ Error in test: {e}")
        import traceback
        traceback.print_exc()
        return False, False

if __name__ == "__main__":
    text_success, audio_success = test_analyze_and_speak()
    print(f"\nTest results:")
    print(f"Analysis text: {'✓' if text_success else '✗'}")
    print(f"Audio file: {'✓' if audio_success else '✗'}")