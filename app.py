import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
from pydub import AudioSegment
from pydub.playback import play
import tempfile

# Initialize speech recognizer, translator
recognizer = sr.Recognizer()
translator = Translator()

# UI Components
st.title("Real-Time Speech-to-Speech Translation")
source_lang = st.selectbox("Select Source Language", ("en", "es", "fr", "de"))
target_lang = st.selectbox("Select Target Language", ("en", "es", "fr", "de"))

if st.button("Start Recording"):
    with sr.Microphone() as source:
        st.write("Listening...")
        audio = recognizer.listen(source)

    try:
        st.write("Recognizing...")
        text = recognizer.recognize_google(audio, language=source_lang)
        st.write(f"Recognized Text: {text}")

        st.write("Translating...")
        translated_text = translator.translate(text, src=source_lang, dest=target_lang).text
        st.write(f"Translated Text: {translated_text}")

        st.write("Converting to Speech...")
        tts = gTTS(translated_text, lang=target_lang)
        with tempfile.NamedTemporaryFile(delete=True) as fp:
            tts.save(fp.name)
            audio_segment = AudioSegment.from_file(fp.name)
            st.write("Playing...")
            play(audio_segment)

    except Exception as e:
        st.write(f"Error: {e}")
