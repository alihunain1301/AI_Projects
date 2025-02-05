import speech_recognition as sr
import pyttsx3 as p
import threading

class conversation:
    def __init__(self):
        self.r = sr.Recognizer()
        self.engine = p.init()
        self.is_male_voice = True  # Default voice is male
        self.set_voice()  # Initialize the voice

    def set_voice(self):
        """Set the voice based on the is_male_voice attribute."""
        voices = self.engine.getProperty('voices')
        if self.is_male_voice:
            self.engine.setProperty('voice', voices[0].id)  # Male voice
        else:
            self.engine.setProperty('voice', voices[1].id)  # Female voice

    def toggle_voice(self):
        """Toggle between male and female voices."""
        self.is_male_voice = not self.is_male_voice
        self.set_voice()

    def speak(self, text):  
            def run_tts():
                self.engine.say(text)
                self.engine.runAndWait()

    
            tts_thread = threading.Thread(target=run_tts)
            tts_thread.start()
    def listen(self):
        """Listen and recognize speech."""
        with sr.Microphone() as source:
            self.r.energy_threshold = 1000
            self.r.adjust_for_ambient_noise(source, duration=1.2)
            print("Listening...")
            audio = self.r.listen(source)
        text = self.r.recognize_google(audio)
        print(text)
        return text
