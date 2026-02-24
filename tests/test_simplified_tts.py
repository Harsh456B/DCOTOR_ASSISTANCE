import asyncio
import edge_tts
import tempfile
import os

async def test_simplified_implementation():
    """Test a simplified implementation without pitch parameter"""
    try:
        text = "This is a test of the simplified Edge TTS implementation."
        voice = "en-US-GuyNeural"
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        output_path = temp_file.name
        temp_file.close()
        
        print(f"Creating audio file at: {output_path}")
        print(f"Text: {text}")
        print(f"Voice: {voice}")
        
        # Simplified implementation (without pitch)
        communicate = edge_tts.Communicate(
            text,
            voice,
            rate="+5%",
            volume="+10%"
        )
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
        print(f"✗ Error in simplified implementation: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_no_parameters():
    """Test with no additional parameters"""
    try:
        text = "This is a test with no additional parameters."
        voice = "en-US-GuyNeural"
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
        output_path = temp_file.name
        temp_file.close()
        
        print(f"Creating audio file at: {output_path}")
        print(f"Text: {text}")
        print(f"Voice: {voice}")
        
        # No additional parameters
        communicate = edge_tts.Communicate(text, voice)
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
        print(f"✗ Error in no parameters implementation: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing simplified Edge TTS implementation...")
    result1 = asyncio.run(test_simplified_implementation())
    print(f"Simplified test result: {result1}")
    
    print("\nTesting no parameters implementation...")
    result2 = asyncio.run(test_no_parameters())
    print(f"No parameters test result: {result2}")