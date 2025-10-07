from dotenv import load_dotenv
import os

load_dotenv()

import streamlit as st
from agent import create_rag_agent, ask_question

from gtts import gTTS
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
    """, unsafe_allow_html=True)

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
        background-color: #F5F5F0 !important;
    }
    [data-testid="stSidebar"] .stMarkdown, [data-testid="stSidebar"] p {
        color: #1E1E1E !important;
    }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .viewerBadge_container__r5tak {display: none !important;}
    header[data-testid="stHeader"] {display: none !important;}
    .stDeployButton {display: none;}
    </style>
    """, unsafe_allow_html=True)

# Sidebar for API key and file upload
# Load API keys from environment
openai_key = os.getenv("OPENAI_API_KEY")
openrouter_key = os.getenv("OPENROUTER_API_KEY")

# Initialize the agent when file is uploaded
# Pre-load the hatchery document
hatchery_doc = "CDFW-Feather River Fish Hatchery.docx"  # Your main document filename

if openai_key and openrouter_key and os.path.exists(hatchery_doc):
    # Create agent if not already created
    if "qa_chain" not in st.session_state:
        with st.spinner("Loading hatchery information..."):
            st.session_state.qa_chain = create_rag_agent(hatchery_doc, openai_key, openrouter_key)

# Chat interface
if "messages" not in st.session_state:
    welcome_msg = """Welcome to the Feather River Fish Hatchery managed by California Department of Fish and Wildlife. I'm Helen, your virtual interpreter.

**Try asking questions like:**
- How does the hatchery work?
- Tell me about chinook salmon
- Show me the fish ladder
- What happens during spawning?
- Explain the salmon lifecycle
- How many fish does the hatchery raise?"""
    st.session_state.messages = [{"role": "assistant", "content": welcome_msg}]

# Display chat history
for message in st.session_state.messages:
    avatar = "helen-avatar.png" if message["role"] == "assistant" else None
    with st.chat_message(message["role"], avatar=avatar):
        st.write(message["content"])
        if "image" in message and message["image"]:
            st.image(message["image"], width=400)

# Chat input
if prompt := st.chat_input("Ask about the hatchery..."):
    if "qa_chain" not in st.session_state:
        st.warning("Please upload a document and enter your API key first.")
    else:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)
        
        # Get agent response
        with st.chat_message("assistant", avatar="helen-avatar.png"):
            with st.spinner("Thinking..."):
                answer, image_path = ask_question(st.session_state.qa_chain, prompt)
                st.write(answer)
                # Add speak button
                if answer and answer.strip():
                    tts = gTTS(text=answer, lang='en', slow=False)
                    tts.save("response.mp3")
                    with open("response.mp3", "rb") as audio_file:
                        audio_bytes = audio_file.read()
                    st.audio(audio_bytes, format="audio/mp3", autoplay=True)
                # Show image if found
                if image_path:
                    st.image(image_path, width=800)
        
        # Add assistant message
        st.session_state.messages.append({"role": "assistant", "content": answer, "image": image_path})