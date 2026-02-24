import asyncio
import tempfile
import os
from gtts import gTTS

def test_gtts_implementation():
    """Test gTTS implementation"""
    try:
        text = "This is a test of the gTTS implementation."
        lang = "en"
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        output_path = temp_file.name
        temp_file.close()
        
        print(f"Creating audio file at: {output_path}")
        print(f"Text: {text}")
        print(f"Language: {lang}")
        
        # Create gTTS object and save
        tts = gTTS(text, lang=lang)
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
        print(f"✗ Error in gTTS implementation: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing gTTS implementation...")
    result = test_gtts_implementation()
    print(f"gTTS test result: {result}")