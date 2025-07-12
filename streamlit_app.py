import streamlit as st
import os
from gemini_app import GeminiVertexAI
from PIL import Image
import io

# Page configuration
st.set_page_config(
    page_title="Gemini 2.0 Vertex AI App",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        margin-bottom: 2rem;
        border-radius: 10px;
    }
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 600;
    }
    .stButton > button:hover {
        background: linear-gradient(90deg, #764ba2 0%, #667eea 100%);
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'gemini_client' not in st.session_state:
    st.session_state.gemini_client = None
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_model' not in st.session_state:
    st.session_state.current_model = "gemini-2.0-flash-exp"

def initialize_gemini():
    """Initialize Gemini client with project ID"""
    project_id = st.session_state.get('project_id', '')
    
    if not project_id:
        st.error("Please enter your Google Cloud Project ID in the sidebar")
        return None
    
    try:
        # Handle service account credentials for cloud deployment
        if hasattr(st, 'secrets') and 'GOOGLE_APPLICATION_CREDENTIALS_JSON' in st.secrets:
            import json
            import tempfile
            
            # Create temporary credentials file
            creds_dict = json.loads(st.secrets['GOOGLE_APPLICATION_CREDENTIALS_JSON'])
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
                json.dump(creds_dict, f)
                os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = f.name
        
        client = GeminiVertexAI(project_id=project_id)
        return client
    except Exception as e:
        st.error(f"Failed to initialize Gemini client: {str(e)}")
        return None

def main():
    # Header
    st.markdown('<div class="main-header"><h1>🚀 Gemini 2.0 Vertex AI App</h1><p>Interact with Gemini 2.0 models using Google Cloud Vertex AI</p></div>', unsafe_allow_html=True)
    
    # Sidebar configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Project ID input
        default_project_id = ""
        if hasattr(st, 'secrets') and 'GOOGLE_CLOUD_PROJECT' in st.secrets:
            default_project_id = st.secrets['GOOGLE_CLOUD_PROJECT']
        else:
            default_project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "")
        
        project_id = st.text_input(
            "Google Cloud Project ID",
            value=default_project_id,
            help="Enter your Google Cloud Project ID"
        )
        st.session_state.project_id = project_id
        
        # Initialize client button
        if st.button("Initialize Gemini Client"):
            st.session_state.gemini_client = initialize_gemini()
            if st.session_state.gemini_client:
                st.success("✅ Gemini client initialized successfully!")
        
        # Model selection
        if st.session_state.gemini_client:
            st.subheader("🤖 Model Selection")
            models = list(st.session_state.gemini_client.models.keys())
            selected_model = st.selectbox(
                "Choose Model",
                models,
                index=models.index(st.session_state.current_model) if st.session_state.current_model in models else 0
            )
            
            if selected_model != st.session_state.current_model:
                st.session_state.gemini_client.set_model(selected_model)
                st.session_state.current_model = selected_model
                st.success(f"Model switched to: {selected_model}")
        
        # Generation parameters
        st.subheader("🎛️ Generation Parameters")
        temperature = st.slider("Temperature", 0.0, 2.0, 0.7, 0.1)
        max_tokens = st.slider("Max Output Tokens", 256, 8192, 2048, 256)
        top_p = st.slider("Top-p", 0.0, 1.0, 0.95, 0.05)
        top_k = st.slider("Top-k", 1, 100, 40, 1)
    
    # Main content area
    if not st.session_state.gemini_client:
        st.info("👈 Please configure your Google Cloud Project ID and initialize the Gemini client in the sidebar to get started.")
        return
    
    # Tab navigation
    tab1, tab2, tab3 = st.tabs(["💬 Text Generation", "🖼️ Vision & Text", "🗣️ Chat"])
    
    with tab1:
        st.header("Text Generation")
        st.write("Generate text responses using Gemini 2.0")
        
        prompt = st.text_area(
            "Enter your prompt:",
            height=150,
            placeholder="Type your question or prompt here..."
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🚀 Generate", key="generate_text"):
                if prompt:
                    with st.spinner("Generating response..."):
                        response = st.session_state.gemini_client.generate_text(
                            prompt,
                            temperature=temperature,
                            max_output_tokens=max_tokens,
                            top_p=top_p,
                            top_k=top_k
                        )
                        st.success("✅ Response generated!")
                        st.markdown("### Response:")
                        st.write(response)
                else:
                    st.error("Please enter a prompt")
    
    with tab2:
        st.header("Vision & Text Generation")
        st.write("Upload images and ask questions about them")
        
        uploaded_files = st.file_uploader(
            "Upload images",
            accept_multiple_files=True,
            type=['png', 'jpg', 'jpeg', 'gif', 'bmp', 'webp']
        )
        
        if uploaded_files:
            st.write("### Uploaded Images:")
            cols = st.columns(min(len(uploaded_files), 3))
            for i, uploaded_file in enumerate(uploaded_files):
                with cols[i % 3]:
                    image = Image.open(uploaded_file)
                    st.image(image, caption=uploaded_file.name, use_container_width=True)
        
        vision_prompt = st.text_area(
            "Enter your prompt about the images:",
            height=100,
            placeholder="Describe what you see in the images, analyze them, or ask specific questions..."
        )
        
        if st.button("🔍 Analyze Images", key="analyze_images"):
            if uploaded_files and vision_prompt:
                with st.spinner("Analyzing images..."):
                    # Save uploaded files temporarily
                    temp_paths = []
                    for uploaded_file in uploaded_files:
                        temp_path = f"temp_{uploaded_file.name}"
                        with open(temp_path, "wb") as f:
                            f.write(uploaded_file.getbuffer())
                        temp_paths.append(temp_path)
                    
                    try:
                        response = st.session_state.gemini_client.generate_with_images(
                            vision_prompt,
                            temp_paths,
                            temperature=temperature,
                            max_output_tokens=max_tokens,
                            top_p=top_p,
                            top_k=top_k
                        )
                        st.success("✅ Analysis complete!")
                        st.markdown("### Analysis Result:")
                        st.write(response)
                    finally:
                        # Clean up temporary files
                        for temp_path in temp_paths:
                            if os.path.exists(temp_path):
                                os.remove(temp_path)
            else:
                st.error("Please upload images and enter a prompt")
    
    with tab3:
        st.header("Chat Conversation")
        st.write("Have a conversation with Gemini 2.0")
        
        # Display chat history
        chat_container = st.container()
        with chat_container:
            for i, message in enumerate(st.session_state.chat_history):
                if message["role"] == "user":
                    st.markdown(f"**You:** {message['content']}")
                else:
                    st.markdown(f"**Assistant:** {message['content']}")
                st.markdown("---")
        
        # Chat input
        user_input = st.text_input(
            "Type your message:",
            placeholder="Ask me anything...",
            key="chat_input"
        )
        
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("💬 Send", key="send_message"):
                if user_input:
                    # Add user message to history
                    st.session_state.chat_history.append({"role": "user", "content": user_input})
                    
                    with st.spinner("Thinking..."):
                        response = st.session_state.gemini_client.chat_conversation(
                            st.session_state.chat_history,
                            temperature=temperature,
                            max_output_tokens=max_tokens,
                            top_p=top_p,
                            top_k=top_k
                        )
                        
                        # Add assistant response to history
                        st.session_state.chat_history.append({"role": "assistant", "content": response})
                    
                    st.rerun()
        
        with col2:
            if st.button("🗑️ Clear Chat", key="clear_chat"):
                st.session_state.chat_history = []
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "Built with ❤️ using Streamlit and Google Cloud Vertex AI"
        "</div>",
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 