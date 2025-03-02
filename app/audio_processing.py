import requests
import os
import pygame
from pydub import AudioSegment
import speech_recognition as sr
from dotenv import load_dotenv
import time

# Load API keys
load_dotenv()
ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
VOICE_ID = os.getenv("VOICE_ID")

def generate_and_play_audio(text, filename):
    """Generate AI voice audio using ElevenLabs and play it using pygame."""
    
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_ID}/stream"
    headers = {"xi-api-key": ELEVENLABS_API_KEY}
    data = {"text": text}

    response = requests.post(url, headers=headers, json=data, stream=True)

    if response.status_code == 200:
        mp3_file = filename + ".mp3"
        wav_file = filename + ".wav"

        # Save the MP3 file
        with open(mp3_file, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    f.write(chunk)

        # Convert MP3 to WAV (pygame only plays WAV)
        audio = AudioSegment.from_mp3(mp3_file)
        audio.export(wav_file, format="wav")

        # Initialize pygame and play audio
        pygame.mixer.init()
        pygame.mixer.music.load(wav_file)
        pygame.mixer.music.play()

        # Wait until the audio finishes playing
        while pygame.mixer.music.get_busy():
            time.sleep(0.1)

        # Stop and quit pygame to release the file
        pygame.mixer.music.stop()
        pygame.mixer.quit()

        # Ensure the file is closed before deleting
        time.sleep(0.5)

        # Cleanup files
        os.remove(mp3_file)
        os.remove(wav_file)
    
    else:
        print(f"Error: {response.status_code}")

def transcribe_user_response():
    """Capture user's speech and convert it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=30)
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Could not understand."
        except sr.RequestError as e:
            return f"Request error: {e}"
