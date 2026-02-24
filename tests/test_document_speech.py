import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_document_to_speech():
    """Test the document to speech functionality which is similar to image analysis"""
    try:
        # Import the function
        from gradio_app_advanced import process_document_to_speech
        import tempfile
        
        # Create a simple text file
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
        temp_file.write("This is a test document for speech conversion. It contains some medical information that should be converted to audio.")
        temp_file.close()
        
        # Create a simple file-like object
        class MockFile:
            def __init__(self, path):
                self.name = path
        
        mock_file = MockFile(temp_file.name)
        
        language = "English"
        gender = "Female"
        
        print("Testing document to speech functionality...")
        print(f"File: {temp_file.name}")
        print(f"Language: {language}")
        print(f"Gender: {gender}")
        
        # Call the function
        status, audio_file = process_document_to_speech(mock_file, language, gender)
        
        print(f"Status: {status}")
        print(f"Audio file: {audio_file}")
        
        if audio_file and os.path.exists(audio_file):
            print("✓ Audio file generated successfully")
            # Check file size
            file_size = os.path.getsize(audio_file)
            print(f"Audio file size: {file_size} bytes")
            # Clean up
            os.unlink(audio_file)
            print("✓ Cleaned up audio file")
            success = True
        else:
            print("✗ Failed to generate audio file")
            success = False
            
        # Clean up the temp text file
        os.unlink(temp_file.name)
        print("✓ Cleaned up temp text file")
        
        return success
        
    except Exception as e:
        print(f"✗ Error in test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_document_to_speech()
    print(f"\nTest result: {'✓ PASS' if success else '✗ FAIL'}")