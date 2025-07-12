#!/usr/bin/env python3
"""
Setup script for the Gemini 2.0 Vertex AI app
"""

import os
import sys
import subprocess

def run_command(command):
    """Run a command and return success status"""
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python version {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    success, output = run_command("pip install -r requirements.txt")
    if success:
        print("✅ Dependencies installed successfully")
        return True
    else:
        print("❌ Failed to install dependencies")
        print(output)
        return False

def check_gcloud():
    """Check if gcloud CLI is available"""
    print("🔍 Checking for Google Cloud CLI...")
    
    # First try the standard command
    success, output = run_command("gcloud --version")
    if success:
        print("✅ Google Cloud CLI is available")
        return True
    
    # On Windows, try the common installation path
    if os.name == 'nt':  # Windows
        import platform
        if platform.system() == 'Windows':
            gcloud_path = os.path.join(os.path.expanduser("~"), "AppData", "Local", "Google", "Cloud SDK", "google-cloud-sdk", "bin", "gcloud.cmd")
            if os.path.exists(gcloud_path):
                print("✅ Found Google Cloud CLI (not in PATH)")
                print(f"   Location: {gcloud_path}")
                print("   Run: PowerShell -ExecutionPolicy Bypass -File fix_gcloud_path.ps1")
                return True
    
    print("⚠️  Google Cloud CLI not found")
    print("   Install from: https://cloud.google.com/sdk/docs/install")
    return False

def setup_environment():
    """Guide user through environment setup"""
    print("\n🔧 Environment Setup")
    print("=" * 50)
    
    # Check for project ID
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("⚠️  GOOGLE_CLOUD_PROJECT environment variable not set")
        print("   Please set it with your Google Cloud project ID:")
        print("   export GOOGLE_CLOUD_PROJECT='your-project-id'")
        return False
    else:
        print(f"✅ GOOGLE_CLOUD_PROJECT: {project_id}")
    
    # Check for authentication
    auth_file = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    if auth_file:
        if os.path.exists(auth_file):
            print(f"✅ Service account key found: {auth_file}")
        else:
            print(f"❌ Service account key file not found: {auth_file}")
            return False
    else:
        print("⚠️  GOOGLE_APPLICATION_CREDENTIALS not set")
        print("   Checking for Application Default Credentials...")
        
        # Try to get ADC info
        success, output = run_command("gcloud auth application-default print-access-token")
        if success:
            print("✅ Application Default Credentials are available")
        else:
            print("❌ No authentication found")
            print("   Please run: gcloud auth application-default login")
            return False
    
    return True

def enable_apis():
    """Enable required APIs"""
    print("\n🚀 Enabling Required APIs")
    print("=" * 50)
    
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    if not project_id:
        print("❌ Project ID not found")
        return False
    
    print(f"Enabling Vertex AI API for project: {project_id}")
    success, output = run_command(f"gcloud services enable aiplatform.googleapis.com --project={project_id}")
    
    if success:
        print("✅ Vertex AI API enabled successfully")
        return True
    else:
        print("❌ Failed to enable Vertex AI API")
        print("   You may need to enable it manually in the Google Cloud Console")
        return False

def test_setup():
    """Test the setup by running a simple example"""
    print("\n🧪 Testing Setup")
    print("=" * 50)
    
    try:
        from gemini_app import GeminiVertexAI
        project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
        
        if not project_id:
            print("❌ Project ID not found")
            return False
        
        print("Creating Gemini client...")
        gemini = GeminiVertexAI(project_id=project_id)
        print("✅ Gemini client created successfully")
        
        print("Testing text generation...")
        response = gemini.generate_text("Hello, this is a test. Please respond briefly.", max_output_tokens=50)
        if response and not response.startswith("Error"):
            print("✅ Text generation test passed")
            print(f"   Response: {response[:100]}...")
            return True
        else:
            print("❌ Text generation test failed")
            print(f"   Error: {response}")
            return False
            
    except Exception as e:
        print(f"❌ Setup test failed: {e}")
        return False

def main():
    """Main setup function"""
    print("🚀 Gemini 2.0 Vertex AI App Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        sys.exit(1)
    
    # Check gcloud
    gcloud_available = check_gcloud()
    
    # Setup environment
    if not setup_environment():
        print("\n❌ Environment setup incomplete")
        print("Please fix the issues above and run setup again")
        sys.exit(1)
    
    # Enable APIs (only if gcloud is available)
    if gcloud_available:
        if not enable_apis():
            print("⚠️  API enabling failed, but you can continue")
    
    # Test setup
    if test_setup():
        print("\n🎉 Setup completed successfully!")
        print("=" * 50)
        print("You can now run:")
        print("  python gemini_app.py        # Command line interface")
        print("  streamlit run streamlit_app.py  # Web interface")
        print("  python example.py           # Example usage")
    else:
        print("\n❌ Setup test failed")
        print("Please check your configuration and try again")
        sys.exit(1)

if __name__ == "__main__":
    main() 