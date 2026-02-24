import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_return_values():
    """Test that our functions return the correct values"""
    try:
        # Test the generate_voice function directly
        from gradio_app_advanced import generate_voice
        
        # Simple test text
        text = "This is a simple test."
        language = "English"
        gender = "Male"
        
        print("Testing generate_voice function...")
        print(f"Input text: {text}")
        print(f"Language: {language}")
        print(f"Gender: {gender}")
        
        # Call the function
        result = generate_voice(text, language, gender)
        
        print(f"Result type: {type(result)}")
        print(f"Result value: {result}")
        
        if result is None:
            print("✗ Function returned None")
            return False
        elif isinstance(result, str) and os.path.exists(result):
            print("✓ Function returned a valid file path")
            # Check if file has content
            file_size = os.path.getsize(result)
            print(f"File size: {file_size} bytes")
            # Clean up
            os.unlink(result)
            print("✓ Cleaned up file")
            return True
        else:
            print(f"✗ Unexpected result: {result}")
            return False
            
    except Exception as e:
        print(f"✗ Error in test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_return_values()
    print(f"\nTest result: {'✓ PASS' if success else '✗ FAIL'}")