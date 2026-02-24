import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Directly test our fixed voice generation function
import asyncio
import tempfile
from gtts import gTTS

def test_direct_gtts():
    """Direct test of gTTS implementation"""
    try:
        text = "This is a direct test of the gTTS implementation."
        lang_code = 'en'
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        output_path = temp_file.name
        temp_file.close()
        
        print(f"Creating audio file at: {output_path}")
        print(f"Text: {text}")
        print(f"Language code: {lang_code}")
        
        # Create gTTS object and save
        tts = gTTS(text, lang=lang_code)
        tts.save(output_path)
        
        print(f"✓ Audio created successfully with gTTS: {output_path}")
        
        # Check if file exists and has content
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            print(f"File size: {file_size} bytes")
            if file_size > 0:
                print("✓ File has content")
                # Clean up
                os.unlink(output_path)
                print("✓ Cleaned up temporary file")
                return True
            else:
                print("✗ File is empty")
                return False
        else:
            print("✗ File was not created")
            return False
            
    except Exception as e:
        print(f"✗ Error in direct gTTS implementation: {e}")
        import traceback
        traceback.print_exc()
        return False

# Test the actual function from our fixed code
def test_fixed_function():
    """Test our fixed generate_voice_multilingual function directly"""
    try:
        # Import the function directly
        from gradio_app_advanced import generate_voice_multilingual
        import asyncio
        
        text = "This is a test of the fixed function."
        language = "English"
        gender = "Male"
        
        print(f"Testing generate_voice_multilingual directly:")
        print(f"Text: {text}")
        print(f"Language: {language}")
        print(f"Gender: {gender}")
        
        # Run the async function
        result = asyncio.run(generate_voice_multilingual(text, language, gender))
        
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
            
    except Exception as e:
        print(f"✗ Error in fixed function test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=== Testing Direct gTTS ===")
    result1 = test_direct_gtts()
    print(f"Direct gTTS test result: {result1}")
    
    print("\n=== Testing Fixed Function ===")
    result2 = test_fixed_function()
    print(f"Fixed function test result: {result2}")