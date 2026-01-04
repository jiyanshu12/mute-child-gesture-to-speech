import pyttsx3
import threading

class Speaker:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.engine.setProperty("rate", 160)
        self.lock = threading.Lock()
        self.is_speaking = False

    def speak(self, text):
        # Do not interrupt current speech
        if self.is_speaking:
            return

        def _run():
            with self.lock:
                self.is_speaking = True
                self.engine.say(text)
                self.engine.runAndWait()
                self.is_speaking = False

        t = threading.Thread(target=_run)
        t.daemon = True
        t.start()

