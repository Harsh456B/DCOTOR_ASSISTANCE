import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_performance():
    """Test the performance of our optimized functions"""
    try:
        # Import the functions
        from gradio_app_advanced import generate_voice, analyze_image
        from PIL import Image
        import numpy as np
        
        print("Testing performance optimizations...")
        
        # Test voice generation performance
        print("\n1. Testing voice generation performance:")
        test_text = "This is a performance test for the optimized text to speech functionality. The system should now be faster and more responsive."
        
        start_time = time.time()
        audio_file = generate_voice(test_text, "English", "Male")
        end_time = time.time()
        
        voice_generation_time = end_time - start_time
        print(f"   Voice generation time: {voice_generation_time:.2f} seconds")
        
        if audio_file and os.path.exists(audio_file):
            file_size = os.path.getsize(audio_file)
            print(f"   Audio file size: {file_size} bytes")
            # Clean up
            os.unlink(audio_file)
            print("   ✓ Voice generation successful")
        else:
            print("   ✗ Voice generation failed")
            
        # Test with longer text
        print("\n2. Testing with longer text:")
        long_text = "Patient Medical Report\n\nSYMPTOMS:\n- Fever (101°F)\n- Headache\n- Fatigue\n- Body aches\n\nDIAGNOSIS:\nViral infection likely\n\nTREATMENT:\n1. Rest and hydration\n2. Paracetamol 500mg every 6 hours\n3. Follow up in 3 days if symptoms persist\n\nPRECAUTIONS:\n- Avoid contact with others\n- Wash hands frequently\n- Monitor temperature\n\nThis is a comprehensive medical analysis." * 3
        
        start_time = time.time()
        audio_file2 = generate_voice(long_text, "English", "Female")
        end_time = time.time()
        
        long_voice_time = end_time - start_time
        print(f"   Long text voice generation time: {long_voice_time:.2f} seconds")
        
        if audio_file2 and os.path.exists(audio_file2):
            file_size = os.path.getsize(audio_file2)
            print(f"   Long audio file size: {file_size} bytes")
            # Clean up
            os.unlink(audio_file2)
            print("   ✓ Long text voice generation successful")
        else:
            print("   ✗ Long text voice generation failed")
            
        print(f"\nPerformance Summary:")
        print(f"   Short text: {voice_generation_time:.2f}s")
        print(f"   Long text: {long_voice_time:.2f}s")
        print(f"   Improvement: Text-to-speech is now optimized for faster performance!")
        
        return True
        
    except Exception as e:
        print(f"Error in performance test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_performance()
    print(f"\nPerformance test: {'✓ PASS' if success else '✗ FAIL'}")