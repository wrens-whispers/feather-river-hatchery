import os
import azure.cognitiveservices.speech as speechsdk

def text_to_speech_azure(text, speech_key, speech_region):
    """
    Convert text to speech using Azure Speech Services
    Returns audio bytes
    """
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
    
    # Set voice - using a warm, friendly female voice
    speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"
    
    # Configure audio output to memory
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    
    # Synthesize speech
    result = speech_synthesizer.speak_text_async(text).get()
    
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        return result.audio_data
    else:
        return None