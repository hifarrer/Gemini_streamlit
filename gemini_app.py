import os
import json
from typing import Optional, List, Dict, Any
from google.cloud import aiplatform
from google.cloud.aiplatform import gapic
import vertexai
from vertexai.generative_models import GenerativeModel, Part, Content
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GeminiVertexAI:
    """
    A class to interact with Gemini 2.0 models using Vertex AI API
    """
    
    def __init__(self, project_id: str, location: str = "us-central1"):
        """
        Initialize the Gemini Vertex AI client
        
        Args:
            project_id: Google Cloud project ID
            location: Vertex AI location (default: us-central1)
        """
        self.project_id = project_id
        self.location = location
        
        # Initialize Vertex AI
        vertexai.init(project=project_id, location=location)
        
        # Available Gemini 2.0 models
        self.models = {
            "gemini-2.0-flash-exp": "gemini-2.0-flash-exp",
            "gemini-2.0-flash-thinking-exp": "gemini-2.0-flash-thinking-exp"
        }
        
        # Initialize the model (default to gemini-2.0-flash-exp)
        self.model = GenerativeModel(self.models["gemini-2.0-flash-exp"])
    
    def set_model(self, model_name: str):
        """
        Set the Gemini model to use
        
        Args:
            model_name: Name of the model ('gemini-2.0-flash-exp' or 'gemini-2.0-flash-thinking-exp')
        """
        if model_name not in self.models:
            raise ValueError(f"Model {model_name} not supported. Available models: {list(self.models.keys())}")
        
        self.model = GenerativeModel(self.models[model_name])
        print(f"Model set to: {model_name}")
    
    def generate_text(self, prompt: str, **kwargs) -> str:
        """
        Generate text using Gemini 2.0
        
        Args:
            prompt: The text prompt to send to the model
            **kwargs: Additional parameters like temperature, max_output_tokens, etc.
        
        Returns:
            Generated text response
        """
        try:
            # Set default parameters
            generation_config = {
                "temperature": kwargs.get("temperature", 0.7),
                "top_p": kwargs.get("top_p", 0.95),
                "top_k": kwargs.get("top_k", 40),
                "max_output_tokens": kwargs.get("max_output_tokens", 2048),
            }
            
            # Generate response
            response = self.model.generate_content(
                prompt,
                generation_config=generation_config
            )
            
            return response.text
            
        except Exception as e:
            return f"Error generating text: {str(e)}"
    
    def generate_with_images(self, prompt: str, image_paths: List[str], **kwargs) -> str:
        """
        Generate text with image inputs using Gemini 2.0
        
        Args:
            prompt: The text prompt
            image_paths: List of local image file paths
            **kwargs: Additional generation parameters
        
        Returns:
            Generated text response
        """
        try:
            # Prepare content with text and images
            content_parts = [prompt]
            
            for image_path in image_paths:
                if os.path.exists(image_path):
                    with open(image_path, 'rb') as f:
                        image_data = f.read()
                    
                    # Determine MIME type based on file extension
                    mime_type = self._get_mime_type(image_path)
                    content_parts.append(Part.from_data(image_data, mime_type=mime_type))
                else:
                    print(f"Warning: Image file {image_path} not found")
            
            # Set generation parameters
            generation_config = {
                "temperature": kwargs.get("temperature", 0.7),
                "top_p": kwargs.get("top_p", 0.95),
                "top_k": kwargs.get("top_k", 40),
                "max_output_tokens": kwargs.get("max_output_tokens", 2048),
            }
            
            # Generate response
            response = self.model.generate_content(
                content_parts,
                generation_config=generation_config
            )
            
            return response.text
            
        except Exception as e:
            return f"Error generating text with images: {str(e)}"
    
    def chat_conversation(self, messages: List[Dict[str, str]], **kwargs) -> str:
        """
        Have a conversation with Gemini 2.0
        
        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            **kwargs: Additional generation parameters
        
        Returns:
            Generated response
        """
        try:
            # Convert messages to Vertex AI format
            contents = []
            for message in messages:
                role = "user" if message["role"] == "user" else "model"
                contents.append(Content(role=role, parts=[Part.from_text(message["content"])]))
            
            # Start chat
            chat = self.model.start_chat(history=contents[:-1])
            
            # Generate response to the last message
            response = chat.send_message(contents[-1].parts[0].text)
            
            return response.text
            
        except Exception as e:
            return f"Error in chat conversation: {str(e)}"
    
    def _get_mime_type(self, file_path: str) -> str:
        """Get MIME type based on file extension"""
        extension = os.path.splitext(file_path)[1].lower()
        mime_types = {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.gif': 'image/gif',
            '.bmp': 'image/bmp',
            '.webp': 'image/webp'
        }
        return mime_types.get(extension, 'image/jpeg')


def main():
    """
    Main function to demonstrate the Gemini Vertex AI integration
    """
    # Get project ID from environment variable
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT")
    
    if not project_id:
        print("Error: Please set the GOOGLE_CLOUD_PROJECT environment variable")
        return
    
    # Initialize Gemini client
    gemini = GeminiVertexAI(project_id=project_id)
    
    print("🚀 Gemini 2.0 Vertex AI App")
    print("=" * 50)
    
    while True:
        print("\nChoose an option:")
        print("1. Generate text")
        print("2. Generate text with images")
        print("3. Chat conversation")
        print("4. Switch model")
        print("5. Exit")
        
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            prompt = input("Enter your prompt: ")
            print("\n🤖 Generating response...")
            response = gemini.generate_text(prompt)
            print(f"\n✨ Response:\n{response}")
        
        elif choice == "2":
            prompt = input("Enter your prompt: ")
            image_paths = input("Enter image file paths (comma-separated): ").split(",")
            image_paths = [path.strip() for path in image_paths]
            print("\n🤖 Generating response with images...")
            response = gemini.generate_with_images(prompt, image_paths)
            print(f"\n✨ Response:\n{response}")
        
        elif choice == "3":
            print("Chat mode - type 'quit' to exit")
            messages = []
            while True:
                user_input = input("\nYou: ")
                if user_input.lower() == 'quit':
                    break
                
                messages.append({"role": "user", "content": user_input})
                print("🤖 Thinking...")
                response = gemini.chat_conversation(messages)
                print(f"Assistant: {response}")
                messages.append({"role": "assistant", "content": response})
        
        elif choice == "4":
            print("Available models:")
            for i, model in enumerate(gemini.models.keys(), 1):
                print(f"{i}. {model}")
            
            model_choice = input("Enter model number: ").strip()
            try:
                model_index = int(model_choice) - 1
                model_name = list(gemini.models.keys())[model_index]
                gemini.set_model(model_name)
            except (ValueError, IndexError):
                print("Invalid model selection")
        
        elif choice == "5":
            print("Goodbye! 👋")
            break
        
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main() 