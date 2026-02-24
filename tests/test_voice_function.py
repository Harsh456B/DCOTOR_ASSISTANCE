import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the functions we need to test
import asyncio
import tempfile
from gradio_app_advanced import generate_voice_multilingual

async def test_generate_voice():
    """Test the generate_voice_multilingual function"""
    print("Testing generate_voice_multilingual function...")
    
    # Test with simple English text
    text = "This is a test of the voice generation function."
    language = "English"
    gender = "Male"
    
    print(f"Input text: {text}")
    print(f"Language: {language}")
    print(f"Gender: {gender}")
    
    result = await generate_voice_multilingual(text, language, gender)
    
    if result:
        print(f"✓ Success! Audio file created at: {result}")
        # Check file size
        file_size = os.path.getsize(result)
        print(f"Audio file size: {file_size} bytes")
        # Clean up
        os.unlink(result)
        print("✓ Cleaned up temporary file")
        return True
    else:
        print("✗ Failed to generate audio")
        return False

if __name__ == "__main__":
    result = asyncio.run(test_generate_voice())
    print(f"Test result: {result}")