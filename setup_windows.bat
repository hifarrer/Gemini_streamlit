@echo off
echo 🚀 Gemini 2.0 Vertex AI App - Windows Setup
echo ================================================

REM Set your Google Cloud Project ID here
set GOOGLE_CLOUD_PROJECT=endless-codex-465716-v9

REM Optional: Set path to service account key file
REM set GOOGLE_APPLICATION_CREDENTIALS=path\to\your\key.json

REM Optional: Set Vertex AI location
set VERTEX_AI_LOCATION=us-central1

echo ✅ Environment variables set for this session:
echo    GOOGLE_CLOUD_PROJECT=%GOOGLE_CLOUD_PROJECT%
echo    VERTEX_AI_LOCATION=%VERTEX_AI_LOCATION%

REM Check if service account key is set
if defined GOOGLE_APPLICATION_CREDENTIALS (
    echo    GOOGLE_APPLICATION_CREDENTIALS=%GOOGLE_APPLICATION_CREDENTIALS%
) else (
    echo    GOOGLE_APPLICATION_CREDENTIALS=Not set (using Application Default Credentials)
)

echo.
echo 🔧 Now you can run:
echo    python setup.py
echo    python gemini_app.py
echo    streamlit run streamlit_app.py
echo.

REM Keep the window open
pause 