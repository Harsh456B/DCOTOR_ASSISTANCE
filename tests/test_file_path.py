import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_audio_file_path():
    """Test that our audio file path is compatible with Gradio"""
    try:
        # Import the function
        from gradio_app_advanced import generate_voice
        import tempfile
        
        # Simple test text
        text = "This is a test to verify the audio file path compatibility with Gradio."
        language = "English"
        gender = "Male"
        
        print("Testing audio file path compatibility...")
        print(f"Input text: {text}")
        print(f"Language: {language}")
        print(f"Gender: {gender}")
        
        # Call the function
        result = generate_voice(text, language, gender)
        
        print(f"Result: {result}")
        print(f"Result type: {type(result)}")
        
        if result is None:
            print("✗ Function returned None")
            return False
            
        if not isinstance(result, str):
            print(f"✗ Expected string, got {type(result)}")
            return False
            
        if not os.path.exists(result):
            print(f"✗ File does not exist: {result}")
            return False
            
        # Check if it's an absolute path
        if not os.path.isabs(result):
            print(f"✗ Path is not absolute: {result}")
            return False
            
        # Check file extension
        _, ext = os.path.splitext(result)
        if ext.lower() != '.mp3':
            print(f"✗ File extension is not .mp3: {ext}")
            return False
            
        # Check file size
        file_size = os.path.getsize(result)
        print(f"File size: {file_size} bytes")
        
        if file_size == 0:
            print("✗ File is empty")
            os.unlink(result)
            return False
            
        print("✓ File path is compatible with Gradio")
        
        # Clean up
        os.unlink(result)
        print("✓ Cleaned up file")
        
        return True
        
    except Exception as e:
        print(f"✗ Error in test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_audio_file_path()
    print(f"\nTest result: {'✓ PASS' if success else '✗ FAIL'}")