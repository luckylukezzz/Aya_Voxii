import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from audiogen import VoiceRecorder, voiceplayer
from time import sleep
from config import push_to_talk_key, target_lang, character
from api.deeptranslate import deeptrans
from api.voicevoxRequests import voiceoutput
from api.deepgram_transcribe import deepgram_tc
import importlib

class MainThread(QThread):
    def __init__(self, window):
        super().__init__()
        self.running = False
        self.recorder = None
        self.window = window

    def run(self):
        self.running = True
        self.recorder = VoiceRecorder(push_to_talk_key)
        while self.running:
            if self.window.key_pressed:
                self.recorder.start_recording()
                while self.window.key_pressed and self.running:
                    sleep(0.1)
                self.recorder.stop_recording()

                engtext = deepgram_tc()
                print(engtext)
                jptext = deeptrans(engtext)
                print(jptext)
                voiceoutput(jptext, character)
                voiceplayer()
            sleep(0.1)

    def stop(self):
        self.running = False
        if self.recorder:
            self.recorder.stream.close()
            self.recorder.audio.terminate()

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.main_thread = None
        self.key_pressed = False

    def initUI(self):
        self.setWindowTitle('Voice Translator')
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        self.play_button = QPushButton('Play', self)
        self.play_button.clicked.connect(self.toggle_main)
        layout.addWidget(self.play_button)

        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel('Push-to-talk key:'))
        self.ptt_input = QLineEdit(push_to_talk_key)
        form_layout.addWidget(self.ptt_input)
        layout.addLayout(form_layout)

        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel('Target language:'))
        self.lang_input = QLineEdit(target_lang)
        form_layout.addWidget(self.lang_input)
        layout.addLayout(form_layout)

        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel('Character:'))
        self.char_input = QLineEdit(str(character))
        form_layout.addWidget(self.char_input)
        layout.addLayout(form_layout)

        self.save_button = QPushButton('Save Config', self)
        self.save_button.clicked.connect(self.save_config)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def toggle_main(self):
        if self.main_thread and self.main_thread.running:
            self.main_thread.stop()
            self.main_thread.wait()
            self.main_thread = None
            self.play_button.setText('Play')
            self.enable_inputs(True)
        else:
            self.main_thread = MainThread(self)
            self.main_thread.start()
            self.play_button.setText('Stop')
            self.enable_inputs(False)

    def save_config(self):
        global push_to_talk_key, target_lang, character
        push_to_talk_key = self.ptt_input.text()
        target_lang = self.lang_input.text()
        character = int(self.char_input.text())

        with open('config.py', 'w') as f:
            f.write(f"push_to_talk_key = '{push_to_talk_key}'\n")
            f.write(f"target_lang = '{target_lang}'\n")
            f.write(f"character = {character}\n")

        importlib.reload(sys.modules['config'])

    def enable_inputs(self, enabled):
        self.ptt_input.setEnabled(enabled)
        self.lang_input.setEnabled(enabled)
        self.char_input.setEnabled(enabled)
        self.save_button.setEnabled(enabled)

    def keyPressEvent(self, event):
        if event.text() == push_to_talk_key:
            self.key_pressed = True

    def keyReleaseEvent(self, event):
        if event.text() == push_to_talk_key:
            self.key_pressed = False

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())