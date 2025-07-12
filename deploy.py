#!/usr/bin/env python3
"""
Deployment helper script for Gemini 2.0 Web App
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def run_command(command, check=True):
    """Run a command and return the result"""
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        return False, "", str(e)

def check_prerequisites():
    """Check if prerequisites are met"""
    print("🔍 Checking prerequisites...")
    
    # Check if git is available
    success, _, _ = run_command("git --version", check=False)
    if not success:
        print("❌ Git is not installed or not available")
        return False
    
    # Check if we're in a git repository
    success, _, _ = run_command("git status", check=False)
    if not success:
        print("❌ Not in a git repository. Please run 'git init' first")
        return False
    
    # Check if service account key exists
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("❌ GOOGLE_CLOUD_PROJECT environment variable not set")
        return False
    
    print("✅ Prerequisites check passed")
    return True

def prepare_for_deployment():
    """Prepare repository for deployment"""
    print("📦 Preparing for deployment...")
    
    # Check if there are uncommitted changes
    success, stdout, _ = run_command("git status --porcelain", check=False)
    if success and stdout.strip():
        print("⚠️  You have uncommitted changes. Committing them now...")
        run_command("git add .")
        run_command('git commit -m "Prepare for deployment"')
    
    # Check if requirements.txt exists
    if not Path("requirements.txt").exists():
        print("❌ requirements.txt not found")
        return False
    
    # Check if streamlit_app.py exists
    if not Path("streamlit_app.py").exists():
        print("❌ streamlit_app.py not found")
        return False
    
    print("✅ Repository prepared for deployment")
    return True

def deploy_to_streamlit_cloud():
    """Guide user through Streamlit Cloud deployment"""
    print("\n🌟 Deploying to Streamlit Cloud")
    print("=" * 50)
    
    print("1. Push your code to GitHub:")
    print("   git push origin main")
    
    print("\n2. Go to https://share.streamlit.io")
    print("3. Sign in with GitHub")
    print("4. Click 'New app'")
    print("5. Select your repository")
    print("6. Choose 'streamlit_app.py' as the main file")
    print("7. Click 'Deploy'")
    
    print("\n8. Configure secrets in Streamlit Cloud:")
    print("   - Go to Settings → Secrets")
    print("   - Add the following secrets:")
    
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    print(f"""
GOOGLE_CLOUD_PROJECT = "{project_id}"
VERTEX_AI_LOCATION = "us-central1"

# Paste your service account JSON here
GOOGLE_APPLICATION_CREDENTIALS_JSON = '''
{{
  "type": "service_account",
  "project_id": "{project_id}",
  "private_key_id": "...",
  "private_key": "...",
  "client_email": "...",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "..."
}}
'''
    """)
    
    print("\n✅ Your app will be available at: https://your-app-name.streamlit.app")

def deploy_to_google_cloud_run():
    """Guide user through Google Cloud Run deployment"""
    print("\n🔥 Deploying to Google Cloud Run")
    print("=" * 50)
    
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    
    print("1. Enable required services:")
    print("   gcloud services enable run.googleapis.com")
    print("   gcloud services enable containerregistry.googleapis.com")
    
    print("\n2. Build and deploy:")
    print(f"   gcloud builds submit --tag gcr.io/{project_id}/gemini-web-app")
    print(f"""   gcloud run deploy gemini-web-app \\
     --image gcr.io/{project_id}/gemini-web-app \\
     --platform managed \\
     --region us-central1 \\
     --allow-unauthenticated \\
     --port 8501 \\
     --memory 2Gi \\
     --set-env-vars GOOGLE_CLOUD_PROJECT={project_id}""")
    
    print("\n3. Set up service account:")
    print("   gcloud iam service-accounts create gemini-web-app-sa")
    print(f"""   gcloud projects add-iam-policy-binding {project_id} \\
     --member="serviceAccount:gemini-web-app-sa@{project_id}.iam.gserviceaccount.com" \\
     --role="roles/aiplatform.user\"""")
    print(f"""   gcloud run services update gemini-web-app \\
     --service-account gemini-web-app-sa@{project_id}.iam.gserviceaccount.com \\
     --region us-central1""")

def deploy_to_railway():
    """Guide user through Railway deployment"""
    print("\n🚢 Deploying to Railway")
    print("=" * 50)
    
    print("1. Go to https://railway.app")
    print("2. Sign up/in with GitHub")
    print("3. Click 'Deploy from GitHub repo'")
    print("4. Select your repository")
    print("5. Railway will auto-detect it's a Python app")
    
    print("\n6. Configure environment variables:")
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    print(f"   GOOGLE_CLOUD_PROJECT={project_id}")
    print("   VERTEX_AI_LOCATION=us-central1")
    print("   GOOGLE_APPLICATION_CREDENTIALS_JSON=<your-service-account-json>")

def main():
    """Main deployment function"""
    print("🚀 Gemini 2.0 Web App Deployment Helper")
    print("=" * 50)
    
    if not check_prerequisites():
        sys.exit(1)
    
    if not prepare_for_deployment():
        sys.exit(1)
    
    print("\n📋 Choose your deployment platform:")
    print("1. Streamlit Cloud (Free & Easy)")
    print("2. Google Cloud Run (Scalable)")
    print("3. Railway (Modern)")
    print("4. Show all options")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        deploy_to_streamlit_cloud()
    elif choice == "2":
        deploy_to_google_cloud_run()
    elif choice == "3":
        deploy_to_railway()
    elif choice == "4":
        deploy_to_streamlit_cloud()
        deploy_to_google_cloud_run()
        deploy_to_railway()
    else:
        print("Invalid choice. Please run the script again.")
        return
    
    print("\n✅ Deployment guide completed!")
    print("📚 For detailed instructions, see DEPLOYMENT.md")

if __name__ == "__main__":
    main() 