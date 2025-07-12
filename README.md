# 🚀 Gemini 2.0 Vertex AI App

A comprehensive Python application for interacting with Google's Gemini 2.0 models using the Vertex AI API. This app provides both command-line and web interfaces for text generation, image analysis, and chat conversations.

## ✨ Features

- **Text Generation**: Generate high-quality text responses using Gemini 2.0
- **Vision & Text**: Analyze images and generate text based on visual content
- **Chat Conversations**: Have interactive conversations with context preservation
- **Multiple Models**: Support for both Gemini 2.0 Flash and Gemini 2.0 Flash Thinking models
- **Web Interface**: Beautiful Streamlit web app with modern UI
- **Command Line**: Interactive CLI for terminal-based usage
- **Configurable Parameters**: Adjust temperature, top-p, top-k, and max tokens

## 🛠️ Prerequisites

Before you begin, ensure you have:

1. **Google Cloud Account** with billing enabled
2. **Google Cloud Project** with Vertex AI API enabled
3. **Authentication** set up (Service Account or Application Default Credentials)
4. **Python 3.8+** installed on your system

## 📦 Installation

1. **Clone or download** this repository
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🔧 Setup

### 1. Google Cloud Setup

#### Enable Vertex AI API:
```bash
gcloud services enable aiplatform.googleapis.com
```

#### Set up authentication (choose one method):

**Method A: Service Account Key (Recommended)**
```bash
# Create a service account
gcloud iam service-accounts create gemini-app-sa

# Grant necessary permissions
gcloud projects add-iam-policy-binding YOUR_PROJECT_ID \
    --member="serviceAccount:gemini-app-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com" \
    --role="roles/aiplatform.user"

# Create and download key
gcloud iam service-accounts keys create key.json \
    --iam-account=gemini-app-sa@YOUR_PROJECT_ID.iam.gserviceaccount.com
```

**Method B: Application Default Credentials**
```bash
gcloud auth application-default login
```

### 2. Environment Configuration

Set your environment variables:

```bash
# Required
export GOOGLE_CLOUD_PROJECT="your-project-id"

# Optional (if using service account key)
export GOOGLE_APPLICATION_CREDENTIALS="path/to/key.json"

# Optional (default: us-central1)
export VERTEX_AI_LOCATION="us-central1"
```

**Windows (PowerShell):**
```powershell
$env:GOOGLE_CLOUD_PROJECT="your-project-id"
$env:GOOGLE_APPLICATION_CREDENTIALS="path\to\key.json"
```

## 🚀 Usage

### Command Line Interface

Run the interactive CLI:
```bash
python gemini_app.py
```

The CLI provides options for:
- Text generation
- Image analysis
- Chat conversations
- Model switching

### Web Interface (Streamlit)

Launch the web app:
```bash
streamlit run streamlit_app.py
```

Then open your browser to `http://localhost:8501`

The web interface includes:
- **Text Generation Tab**: Simple text prompts
- **Vision & Text Tab**: Upload images and ask questions
- **Chat Tab**: Interactive conversations
- **Sidebar**: Configuration and model selection

## 🎯 Examples

### Basic Text Generation
```python
from gemini_app import GeminiVertexAI

# Initialize client
gemini = GeminiVertexAI(project_id="your-project-id")

# Generate text
response = gemini.generate_text("Explain quantum computing in simple terms")
print(response)
```

### Image Analysis
```python
# Analyze images
response = gemini.generate_with_images(
    "What do you see in this image?",
    ["path/to/image.jpg"]
)
print(response)
```

### Chat Conversation
```python
# Have a conversation
messages = [
    {"role": "user", "content": "Hello! How are you?"},
    {"role": "assistant", "content": "I'm doing well, thank you!"},
    {"role": "user", "content": "Can you help me with Python?"}
]

response = gemini.chat_conversation(messages)
print(response)
```

## 🎛️ Configuration

### Available Models

- **gemini-2.0-flash-exp**: Fast and efficient for general tasks
- **gemini-2.0-flash-thinking-exp**: Enhanced reasoning capabilities

### Generation Parameters

- **Temperature** (0.0-2.0): Controls randomness (lower = more focused)
- **Top-p** (0.0-1.0): Nucleus sampling parameter
- **Top-k** (1-100): Number of top tokens to consider
- **Max Output Tokens** (1-8192): Maximum response length

## 📁 Project Structure

```
Gemini2.0/
├── gemini_app.py          # Main application with CLI
├── streamlit_app.py       # Streamlit web interface
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🔧 Troubleshooting

### Common Issues

**1. Authentication Error**
```
Error: Could not automatically determine credentials
```
**Solution**: Set up authentication using service account key or ADC

**2. Project Not Found**
```
Error: Project not found or access denied
```
**Solution**: Verify project ID and ensure Vertex AI API is enabled

**3. Model Not Available**
```
Error: Model not found in location
```
**Solution**: Check if Gemini 2.0 is available in your region (try us-central1)

**4. Permission Denied**
```
Error: Permission denied
```
**Solution**: Ensure your service account has `aiplatform.user` role

### Debug Mode

Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 📊 Performance Tips

1. **Use appropriate temperatures**: Lower for factual content, higher for creative tasks
2. **Optimize token limits**: Set reasonable max_output_tokens to reduce costs
3. **Batch requests**: For multiple similar requests, consider batching
4. **Cache responses**: Store frequently used responses to reduce API calls

## 💰 Cost Optimization

- Monitor usage in Google Cloud Console
- Set up billing alerts
- Use lower token limits when possible
- Consider using the Flash model for faster, cheaper responses

## 🤝 Contributing

Feel free to submit issues, fork the repository, and create pull requests for improvements.

## 📄 License

This project is licensed under the MIT License.

## 🔗 Resources

- [Vertex AI Documentation](https://cloud.google.com/vertex-ai/docs)
- [Gemini API Reference](https://cloud.google.com/vertex-ai/docs/generative-ai/multimodal/overview)
- [Google Cloud Console](https://console.cloud.google.com/)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 📞 Support

For issues related to:
- **Google Cloud/Vertex AI**: Check [Google Cloud Support](https://cloud.google.com/support)
- **This Application**: Create an issue in this repository

---

**Happy coding with Gemini 2.0! 🚀** 