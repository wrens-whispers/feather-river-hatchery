import os
import azure.cognitiveservices.speech as speechsdk
import streamlit as st

def speech_to_text(speech_key, speech_region):
    """
    Capture speech from microphone and convert to text
    Returns the transcribed text or None if error
    """
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    speech_config.speech_recognition_language = "en-US"
    
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
    speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config, audio_config=audio_config)
    
    st.info("🎤 Listening... Speak now!")
    
    result = speech_recognizer.recognize_once_async().get()
    
    if result.reason == speechsdk.ResultReason.RecognizedSpeech:
        return result.text
    elif result.reason == speechsdk.ResultReason.NoMatch:
        st.warning("Sorry, I didn't catch that. Please try again.")
        return None
    elif result.reason == speechsdk.ResultReason.Canceled:
        st.error("Speech recognition canceled. Please try again.")
        return None
    
    return None