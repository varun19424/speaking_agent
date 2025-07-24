import speech_recognition as sr

def get_speech_input():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        audio = r.listen(source)
    try:
        return r.recognize_google(audio)
    except sr.UnknownValueError:
        return "Sorry, I couldn't understand your voice."
    except sr.RequestError:
        return "Speech recognition service error."
