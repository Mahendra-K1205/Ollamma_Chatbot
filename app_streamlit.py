"""
Ollama Chatbot - Streamlit Web GUI
Modern web-based interface for local LLM chat.
"""

import streamlit as st
import os
from ollama_backend import OllamaBackend


def init_session_state():
    """Initialize Streamlit session state."""
    if "backend" not in st.session_state:
        ollama_url = os.getenv("OLLAMA_API_URL", "http://localhost:11434")
        st.session_state.backend = OllamaBackend(base_url=ollama_url)
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "models" not in st.session_state:
        st.session_state.models = []


def load_models():
    """Load available models from Ollama."""
    try:
        models = st.session_state.backend.get_available_models()
        st.session_state.models = models
        return models
    except ConnectionError as e:
        st.error(f"❌ {str(e)}")
        st.info("💡 Make sure Ollama is running: `ollama serve`")
        return []


def clear_chat():
    """Clear chat history."""
    st.session_state.backend.clear_history()
    st.session_state.messages = []
    st.success("✅ Chat cleared!")


def main():
    # Page config
    st.set_page_config(
        page_title="Ollama Chatbot",
        page_icon="🤖",
        layout="wide"
    )
    
    # Custom CSS for modern styling
    st.markdown("""
        <style>
        .stApp {
            background-color: #1e1e1e;
        }
        .stTextInput > div > div > input {
            background-color: #2d2d2d;
            color: white;
        }
        .stSelectbox > div > div > select {
            background-color: #2d2d2d;
            color: white;
        }
        .user-message {
            background-color: #1e3a5f;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            border-left: 4px solid #4fc3f7;
        }
        .bot-message {
            background-color: #1e3a1e;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            border-left: 4px solid #81c784;
        }
        .error-message {
            background-color: #3a1e1e;
            padding: 15px;
            border-radius: 10px;
            margin: 10px 0;
            border-left: 4px solid #e57373;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Initialize
    init_session_state()
    
    # Header
    st.title("🤖 Ollama Chatbot")
    st.markdown("---")
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        # Load models button
        if st.button("🔄 Refresh Models", use_container_width=True):
            with st.spinner("Loading models..."):
                models = load_models()
                if models:
                    st.success(f"✅ Loaded {len(models)} models")
        
        # Model selection
        if not st.session_state.models:
            st.session_state.models = load_models()
        
        if st.session_state.models:
            selected_model = st.selectbox(
                "Select Model",
                st.session_state.models,
                index=0,
                key="model_selector"
            )
            if st.session_state.backend.model != selected_model:
                st.session_state.backend.set_model(selected_model)
                st.info("🔄 Model switched, history cleared")
            st.info(f"📦 Active: **{selected_model}**")
        else:
            st.warning("⚠️ No models available")
        
        st.markdown("---")
        
        # Clear chat button
        if st.button("🗑️ Clear Chat", use_container_width=True):
            clear_chat()
            st.rerun()
        
        st.markdown("---")
        
        # Info
        st.markdown("""
        ### 📖 Instructions
        1. Select a model
        2. Type your message
        3. Press Enter or click Send
        
        ### 💡 Tips
        - Chat history is maintained
        - Use Clear Chat to reset
        - Refresh models if new ones added
        """)
    
    # Chat display area
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="user-message">👤 <b>You:</b><br>{msg["content"]}</div>', 
                          unsafe_allow_html=True)
            elif msg["role"] == "assistant":
                st.markdown(f'<div class="bot-message">🤖 <b>Bot:</b><br>{msg["content"]}</div>', 
                          unsafe_allow_html=True)
            elif msg["role"] == "error":
                st.markdown(f'<div class="error-message">❌ <b>Error:</b><br>{msg["content"]}</div>', 
                          unsafe_allow_html=True)
    
    # Input area
    st.markdown("---")
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "Your message:",
            key="user_input",
            placeholder="Type your message here...",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("📤 Send", use_container_width=True)
    
    # Handle message sending
    if send_button and user_input:
        # Add user message to display
        st.session_state.messages.append({"role": "user", "content": user_input})
        
        # Get bot response
        with st.spinner("🤔 Thinking... (First request may take 1-2 minutes to load model)"):
            try:
                response = st.session_state.backend.send_message(user_input)
                st.session_state.messages.append({"role": "assistant", "content": response})
            except Exception as e:
                st.session_state.messages.append({"role": "error", "content": str(e)})
        
        # Clear input and rerun
        st.rerun()


if __name__ == "__main__":
    main()
