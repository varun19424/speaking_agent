import pyttsx3
import tempfile

def text_to_audio(text: str) -> str:
    engine = pyttsx3.init()
    engine.setProperty('rate', 160)
    engine.setProperty('volume', 1.0)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as f:
        temp_audio_path = f.name

    engine.save_to_file(text, temp_audio_path)
    engine.runAndWait()

    return temp_audio_path
