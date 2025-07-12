#!/usr/bin/env python3
"""
Example script demonstrating how to use the Gemini 2.0 Vertex AI client
"""

import os
from gemini_app import GeminiVertexAI

def main():
    """Main example function"""
    
    # Set your project ID here or use environment variable
    project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "your-project-id-here")
    
    if project_id == "your-project-id-here":
        print("❌ Please set your GOOGLE_CLOUD_PROJECT environment variable or update the project_id in this script")
        return
    
    print(f"🚀 Initializing Gemini 2.0 client for project: {project_id}")
    
    try:
        # Initialize the Gemini client
        gemini = GeminiVertexAI(project_id=project_id)
        print("✅ Client initialized successfully!")
        
        # Example 1: Basic text generation
        print("\n" + "="*50)
        print("📝 Example 1: Basic Text Generation")
        print("="*50)
        
        prompt = "Explain the concept of artificial intelligence in simple terms"
        print(f"Prompt: {prompt}")
        print("\n🤖 Generating response...")
        
        response = gemini.generate_text(prompt, temperature=0.7)
        print(f"\n✨ Response:\n{response}")
        
        # Example 2: Creative writing with higher temperature
        print("\n" + "="*50)
        print("🎨 Example 2: Creative Writing")
        print("="*50)
        
        creative_prompt = "Write a short poem about the future of technology"
        print(f"Prompt: {creative_prompt}")
        print("\n🤖 Generating response...")
        
        creative_response = gemini.generate_text(
            creative_prompt, 
            temperature=1.0,  # Higher temperature for more creativity
            max_output_tokens=500
        )
        print(f"\n✨ Creative Response:\n{creative_response}")
        
        # Example 3: Chat conversation
        print("\n" + "="*50)
        print("💬 Example 3: Chat Conversation")
        print("="*50)
        
        # Simulate a conversation
        messages = [
            {"role": "user", "content": "Hello! I'm learning about machine learning. Can you help me?"},
            {"role": "assistant", "content": "Of course! I'd be happy to help you learn about machine learning. What specific aspect would you like to explore?"},
            {"role": "user", "content": "What's the difference between supervised and unsupervised learning?"}
        ]
        
        print("Chat History:")
        for msg in messages[:-1]:  # Show all but the last message
            role = "You" if msg["role"] == "user" else "Assistant"
            print(f"{role}: {msg['content']}")
        
        print(f"\nYou: {messages[-1]['content']}")
        print("\n🤖 Generating response...")
        
        chat_response = gemini.chat_conversation(messages)
        print(f"\nAssistant: {chat_response}")
        
        # Example 4: Technical explanation with specific parameters
        print("\n" + "="*50)
        print("🔬 Example 4: Technical Explanation")
        print("="*50)
        
        tech_prompt = "Explain how neural networks work, including backpropagation"
        print(f"Prompt: {tech_prompt}")
        print("\n🤖 Generating response...")
        
        tech_response = gemini.generate_text(
            tech_prompt,
            temperature=0.3,  # Lower temperature for factual content
            max_output_tokens=1000,
            top_p=0.8
        )
        print(f"\n✨ Technical Response:\n{tech_response}")
        
        # Example 5: Model switching
        print("\n" + "="*50)
        print("🔄 Example 5: Model Switching")
        print("="*50)
        
        print("Current model: gemini-2.0-flash-exp")
        print("Switching to gemini-2.0-flash-thinking-exp...")
        
        try:
            gemini.set_model("gemini-2.0-flash-thinking-exp")
            
            thinking_prompt = "Solve this step by step: If a train travels 120 miles in 2 hours, and then 180 miles in 3 hours, what is the average speed for the entire trip?"
            print(f"\nPrompt: {thinking_prompt}")
            print("\n🤖 Generating response with thinking model...")
            
            thinking_response = gemini.generate_text(thinking_prompt)
            print(f"\n✨ Thinking Model Response:\n{thinking_response}")
            
        except Exception as e:
            print(f"❌ Error switching models: {e}")
        
        print("\n" + "="*50)
        print("🎉 Examples completed successfully!")
        print("="*50)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Troubleshooting tips:")
        print("1. Make sure your GOOGLE_CLOUD_PROJECT environment variable is set")
        print("2. Ensure you have proper authentication (service account key or ADC)")
        print("3. Check that Vertex AI API is enabled in your project")
        print("4. Verify that Gemini 2.0 models are available in your region")

if __name__ == "__main__":
    main() 