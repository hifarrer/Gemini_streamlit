"""
Configuration settings for the Gemini 2.0 Vertex AI app
"""

import os
from typing import Dict, Any

# Default configuration
DEFAULT_CONFIG = {
    "project_id": os.getenv("GOOGLE_CLOUD_PROJECT", "endless-codex-465716-v9"),
    "location": os.getenv("VERTEX_AI_LOCATION", "us-central1"),
    "default_model": os.getenv("DEFAULT_MODEL", "gemini-2.0-flash-exp"),
    "service_account_key": os.getenv("GOOGLE_APPLICATION_CREDENTIALS", ""),
}

# Generation parameters
GENERATION_CONFIG = {
    "temperature": 0.7,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 2048,
}

# Available models
AVAILABLE_MODELS = {
    "gemini-2.0-flash-exp": {
        "name": "Gemini 2.0 Flash (Experimental)",
        "description": "Fast and efficient model for general tasks",
        "supports_vision": True,
        "supports_chat": True,
    },
    "gemini-2.0-flash-thinking-exp": {
        "name": "Gemini 2.0 Flash Thinking (Experimental)",
        "description": "Model with enhanced reasoning capabilities",
        "supports_vision": True,
        "supports_chat": True,
    }
}

def get_config() -> Dict[str, Any]:
    """Get the current configuration"""
    return DEFAULT_CONFIG.copy()

def update_config(new_config: Dict[str, Any]) -> None:
    """Update the configuration with new values"""
    DEFAULT_CONFIG.update(new_config)

def validate_config() -> bool:
    """Validate the current configuration"""
    required_fields = ["project_id"]
    
    for field in required_fields:
        if not DEFAULT_CONFIG.get(field):
            print(f"❌ Missing required configuration: {field}")
            return False
    
    print("✅ Configuration is valid")
    return True 