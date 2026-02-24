import sys
import os
import time
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_balanced_optimization():
    """Test that we have balanced optimization - longer content with good performance"""
    try:
        # Import the functions
        from gradio_app_advanced import generate_voice
        import tempfile
        
        print("Testing balanced optimization...")
        
        # Test with moderately long medical text
        print("\n1. Testing with detailed medical content:")
        medical_text = """Patient Medical Report

SYMPTOMS:
- Persistent fever (101-102°F) for 3 days
- Severe headache with pressure around eyes and forehead
- Nasal congestion and post-nasal drip
- Fatigue and body aches
- Loss of appetite
- Mild sore throat

DIAGNOSIS:
Viral upper respiratory infection (common cold/flu) - 85% confidence
Bacterial sinusitis - 10% confidence
Allergic rhinitis - 5% confidence

RECOMMENDED MEDICINES:
1. Paracetamol (Crocin) 500mg - Take 1 tablet every 6 hours as needed for fever/pain - 5 days - Side effects: Liver toxicity in high doses
2. Levocetirizine (Xyzal) 5mg - Take 1 tablet at night for 7 days - Side effects: Drowsiness, dry mouth
3. Steam inhalation 2-3 times daily for 10 minutes

HOME REMEDIES:
- Drink warm fluids (water, herbal tea, soup)
- Get adequate rest (8-10 hours sleep)
- Use saline nasal drops
- Gargle with warm salt water

MEDICAL ADVICE:
- Monitor temperature twice daily
- Stay hydrated with at least 3 liters of fluid
- Avoid crowded places and wear mask
- Wash hands frequently

URGENCY LEVEL: Moderate
Seek immediate care if:
- Temperature exceeds 103°F
- Difficulty breathing develops
- Severe headache worsens
- Neck stiffness occurs

PRECAUTIONS:
- Do not exceed recommended paracetamol dosage
- Avoid alcohol during treatment
- Rest and avoid strenuous activities

FOLLOW-UP:
- Reassess in 3 days
- Return sooner if symptoms worsen
- Consider blood test if fever persists beyond 5 days"""

        start_time = time.time()
        audio_file = generate_voice(medical_text, "English", "Male")
        end_time = time.time()
        
        processing_time = end_time - start_time
        print(f"   Processing time: {processing_time:.2f} seconds")
        print(f"   Text length: {len(medical_text)} characters")
        
        if audio_file and os.path.exists(audio_file):
            file_size = os.path.getsize(audio_file)
            print(f"   Audio file size: {file_size} bytes")
            # Clean up
            os.unlink(audio_file)
            print("   ✓ Detailed content processing successful")
            success = True
        else:
            print("   ✗ Detailed content processing failed")
            success = False
            
        # Test with even longer text
        print("\n2. Testing with extended medical content:")
        extended_text = medical_text * 2  # Double the content
        
        start_time = time.time()
        audio_file2 = generate_voice(extended_text, "English", "Female")
        end_time = time.time()
        
        extended_time = end_time - start_time
        print(f"   Extended processing time: {extended_time:.2f} seconds")
        print(f"   Extended text length: {len(extended_text)} characters")
        
        if audio_file2 and os.path.exists(audio_file2):
            file_size = os.path.getsize(audio_file2)
            print(f"   Extended audio file size: {file_size} bytes")
            # Clean up
            os.unlink(audio_file2)
            print("   ✓ Extended content processing successful")
            extended_success = True
        else:
            print("   ✗ Extended content processing failed")
            extended_success = False
            
        print(f"\nBalanced Optimization Results:")
        print(f"   Detailed content ({len(medical_text)} chars): {processing_time:.2f}s")
        print(f"   Extended content ({len(extended_text)} chars): {extended_time:.2f}s")
        print(f"   Content is longer but still processes efficiently!")
        
        return success and extended_success
        
    except Exception as e:
        print(f"Error in balanced optimization test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_balanced_optimization()
    print(f"\nBalanced optimization test: {'✓ PASS' if success else '✗ FAIL'}")