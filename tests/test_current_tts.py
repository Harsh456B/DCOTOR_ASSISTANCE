import asyncio
import edge_tts
import tempfile
import os

async def test_current_implementation():
    """Test the current implementation from gradio_app_advanced.py"""
    try:
        text = "This is a test of the current Edge TTS implementation."
        voice = "en-US-GuyNeural"
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        output_path = temp_file.name
        temp_file.close()
        
        print(f"Creating audio file at: {output_path}")
        
        # Current implementation
        communicate = edge_tts.Communicate(text, voice, rate="+5%", volume="+10%")
        await communicate.save(output_path)
        
        print(f"✓ Audio created successfully: {output_path}")
        
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
        print(f"✗ Error in current implementation: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing current Edge TTS implementation...")
    result = asyncio.run(test_current_implementation())
    print(f"Test result: {result}")