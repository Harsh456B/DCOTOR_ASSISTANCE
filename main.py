"""
AI Doctor Medical Assistance - Main Entry Point

This is the main entry point for the AI Doctor Medical Assistance application.
Run this file to start the application.
"""

import subprocess
import sys
import os

def main():
    """Main function to run the application"""
    print("Starting AI Doctor Medical Assistance...")
    print("Loading application...")
    
    # Add src directory to the Python path
    src_path = os.path.join(os.path.dirname(__file__), 'src')
    sys.path.insert(0, src_path)
    
    try:
        # Change to the src directory and run the main application
        os.chdir(src_path)
        import gradio_app_advanced
        
        # Run the application
        gradio_app_advanced.demo.launch(
            share=False,
            server_port=8080,  # Changed from 7860 to avoid port conflicts
            show_error=True,
            inbrowser=True,
            show_api=False,
            max_threads=8
        )
    except ImportError as e:
        print(f"Error importing the application: {e}")
        print("Trying to run via subprocess from src directory...")
        os.chdir(src_path)
        subprocess.run([sys.executable, 'gradio_app_advanced.py'])
    except Exception as e:
        print(f"Could not start application: {e}")
        print("Make sure you have installed all dependencies and have valid API keys.")

if __name__ == "__main__":
    main()