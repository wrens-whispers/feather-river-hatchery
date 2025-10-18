from dotenv import load_dotenv
import os
load_dotenv()
import streamlit as st

# Initialize language in session state FIRST
if 'language' not in st.session_state:
    st.session_state.language = 'en'

# Force sidebar to be open by default
st.set_page_config(initial_sidebar_state="expanded")

from agent import create_rag_agent, ask_question
from speech_handler import text_to_speech_azure
import base64

# Add CDFW centered logo and banner
st.markdown("""
    <div style='text-align: center;'>
        <img src='data:image/png;base64,{}' width='150'>
    </div>
    """.format(base64.b64encode(open("cdfw-logo.png", "rb").read()).decode()), unsafe_allow_html=True)

st.markdown("""
    <div style='background-color: #046B99; padding: 20px; margin: 10px 0 20px 0; border-bottom: 3px solid #C69C6D; text-align: center;'>
        <h1 style='color: white; margin: 0;'>Feather River Fish Hatchery</h1>
        <p style='color: #C69C6D; margin: 5px 0 0 0;'>California Department of Fish and Wildlife Virtual Interpreter</p>
    </div>
    </div>
    """, unsafe_allow_html=True)
# Sidebar with keywords
with st.sidebar:
    st.header("Topics with Images")
    st.markdown("""
    Ask Helen about any of these topics to see related images:
    
    • chinook  
    • steelhead  
    • trout  
    • eggs  
    • spawning  
    • ladder  
    • lifecycle  
    • fishing  
    • viewing window  
    • habitat  
    • hatchery  
    • upstream  
    • underwater
    """)

# Custom colors
st.markdown("""
    <style>
    .stApp {
        background-color: #F5F5F0 !important;
        color: #1E1E1E !important;
    }
    .stChatMessage [data-testid="stImage"] img[src*="helen-avatar"] {
        width: 80px !important;
        height: 80px !important;
        border-radius: 50%;
    }
    .stMarkdown, p, span, div {
        color: #1E1E1E !important;
    }
    [data-testid="stSidebar"] {
        background-color: #1E1E1E !important;
    }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p, [data-testid="stSidebar"] h2 {
        color: white !important;
    }
    button[kind="header"] {
        background-color: white !important;
        color: #046B99 !important;
    }
    [data-testid="stSidebarNavButton"] button,
    [data-testid="baseButton-header"] {
        background-color: white !important;
        color: #046B99 !important;
    }
    [aria-label="Show sidebar navigation"] {
        background-color: white !important;
        color: #046B99 !important;
        border: 2px solid white !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

openai_key = os.getenv("OPENAI_API_KEY")
openrouter_key = os.getenv("OPENROUTER_API_KEY")

# Initialize the agent when file is uploaded
# Pre-load the hatchery document
hatchery_doc = "CDFW-Feather River Fish Hatchery.docx"  # Your main document filename

if openai_key and openrouter_key and os.path.exists(hatchery_doc):
    # Create agent if not already created
    if "qa_chain" not in st.session_state:
        try:
            with st.spinner("Loading hatchery information..."):
                st.session_state.qa_chain = create_rag_agent(hatchery_doc, openai_key, openrouter_key)
            st.success("✅ Helen is ready!")
        except Exception as e:
            st.error(f"Error loading agent: {str(e)}")
            st.info("Please refresh the page or contact support.")

# Chat interface
if "messages" not in st.session_state:
    welcome_msg = """Welcome to the Feather River Fish Hatchery managed by California Department of Fish and Wildlife. I'm Helen, your virtual interpreter.

**Para intérprete en español, diga 'español'**

**Topics to explore:**
chinook, steelhead, trout, eggs, spawning, ladder, lifecycle, fishing, viewing window, habitat, hatchery, upstream, underwater

**Example questions:**
- How does the hatchery work?
- Where can I see the fish?
- What happens during spawning?"""
    st.session_state.messages = [{"role": "assistant", "content": welcome_msg}]

# Display chat history
for message in st.session_state.messages:
    avatar = "helen-avatar.png" if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])
        if "image" in message and message["image"]:
            st.image(message["image"], width=400)

# Voice input tip
st.warning("⚠️ **Safari users:** If the app won't load, please use Chrome or Firefox for best compatibility.")

# Chat input
if prompt := st.chat_input("Ask about the hatchery..."):
    if "qa_chain" not in st.session_state:
        st.warning("Please upload a document and enter your API key first.")
    else:
        # Check if user is requesting Spanish
        if 'español' in prompt.lower() or 'espanol' in prompt.lower():
            st.session_state.language = 'es'

        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get agent response
        with st.chat_message("assistant", avatar="helen-avatar.png"):
            with st.spinner("Thinking..."):
                answer, image_path = ask_question(st.session_state.qa_chain, prompt)
                st.write(answer)
                # Azure TTS
                if answer and answer.strip():
                    azure_key = os.getenv("AZURE_SPEECH_KEY")
                    azure_region = os.getenv("AZURE_SPEECH_REGION")
                    if azure_key and azure_region:
                        audio_data = text_to_speech_azure(answer, azure_key, azure_region, st.session_state.language)
                        if audio_data:
                            st.audio(audio_data, format="audio/wav", autoplay=True)
                # Show image if found
                if image_path:
                    st.image(image_path, width=800)
        
        # Add assistant message
        st.session_state.messages.append({"role": "assistant", "content": answer, "image": image_path})