import asyncio
import edge_tts

async def test_tts():
    try:
        # Test text
        text = "Hello, this is a test of the text to speech functionality."
        voice = "en-US-GuyNeural"
        
        # Create communicate object
        communicate = edge_tts.Communicate(text, voice)
        print("Communicate object created successfully")
        
        # Save to file
        await communicate.save("test_tts.mp3")
        print("Audio file generated successfully: test_tts.mp3")
        return True
    except Exception as e:
        print(f"Error in TTS generation: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Run the async function
    result = asyncio.run(test_tts())
    print(f"TTS test result: {result}")