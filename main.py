"""
AI Doctor Medical Assistance - Main Entry Point for Render / local

This file runs the FastAPI app defined in src/gradio_app_advanced.py
using uvicorn. Render can call `python main.py` as the start command.
"""

import os

import uvicorn


def main() -> None:
    port = int(os.environ.get("PORT", "8000"))
    # Import here so that environment (.env, API keys) is loaded correctly
    from src.gradio_app_advanced import app

    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    main()