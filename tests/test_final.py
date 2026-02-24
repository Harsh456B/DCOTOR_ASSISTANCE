import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_process_document_to_speech():
    """Test the full document to speech workflow which is similar to image analysis"""
    try:
        # Import the function
        from gradio_app_advanced import process_document_to_speech
        import tempfile
        
        # Create a simple text file
        temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False)
        temp_file.write("Patient Medical Report\n\nSYMPTOMS:\n- Fever (101°F)\n- Headache\n- Fatigue\n\nDIAGNOSIS:\nViral infection likely\n\nTREATMENT:\n1. Rest and hydration\n2. Paracetamol 500mg every 6 hours\n3. Follow up in 3 days if symptoms persist")
        temp_file.close()
        
        # Create a simple file-like object
        class MockFile:
            def __init__(self, path):
                self.name = path
        
        mock_file = MockFile(temp_file.name)
        
        language = "English"
        gender = "Female"
        
        print("Testing full document to speech workflow...")
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
            
            if file_size > 0:
                print("✓ Audio file has content")
                # Clean up
                os.unlink(audio_file)
                print("✓ Cleaned up audio file")
                success = True
            else:
                print("✗ Audio file is empty")
                os.unlink(audio_file)
                success = False
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
    success = test_process_document_to_speech()
    print(f"\nFinal test result: {'✓ PASS - Audio Report functionality is working!' if success else '✗ FAIL'}")