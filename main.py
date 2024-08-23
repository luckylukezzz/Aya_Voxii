import sys
import os
from dotenv import load_dotenv, set_key
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QInputDialog
from PyQt5.QtCore import QThread, Qt
from PyQt5.QtGui import QPixmap, QPalette, QColor, QIcon
from audiogen import VoiceRecorder, voiceplayer
from time import sleep
from config import push_to_talk_key, target_lang, character
from api.deeptranslate import deeptrans
from api.voicevoxRequests import voiceoutput
from api.deepgram_transcribe import deepgram_tc
import importlib

load_dotenv()

character_images = {
    1: "images/1.png",
    2: "images/2.png",
    3: "images/3.png",
    4: "images/4.png",
    5: "images/5.png",
    6: "images/6.png",
    7: "images/7.png",
    8: "images/8.png",
    9: "images/9.png",
    10: "images/10.png",
    
}

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
        self.setWindowTitle('Aya_voxii')
        self.setWindowIcon(QIcon('icon.ico'))
        self.setGeometry(100, 100, 600, 400)

        # Set dark theme
        self.setStyleSheet("""
            QWidget {
                background-color: #2b2b2b;
                color: #ffffff;
            }
            QPushButton {
                background-color: #3d3d3d;
                border: none;
                padding: 5px;
            }
            QLineEdit {
                background-color: #3d3d3d;
                border: none;
                padding: 5px;
            }
        """)

        main_layout = QHBoxLayout()

        # Left side - Image display
        self.image_label = QLabel(self)
        self.image_label.setFixedSize(200, 200)
        self.update_character_image(character)
        main_layout.addWidget(self.image_label)

        # Right side - Controls
        controls_layout = QVBoxLayout()

        self.play_button = QPushButton('Play', self)
        self.play_button.clicked.connect(self.toggle_main)
        controls_layout.addWidget(self.play_button)

        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel('Push-to-talk key:'))
        self.ptt_input = QLineEdit(push_to_talk_key)
        form_layout.addWidget(self.ptt_input)
        controls_layout.addLayout(form_layout)

        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel('Target language:'))
        self.lang_input = QLineEdit(target_lang)
        form_layout.addWidget(self.lang_input)
        controls_layout.addLayout(form_layout)

        form_layout = QHBoxLayout()
        form_layout.addWidget(QLabel('Character:'))
        self.char_input = QLineEdit(str(character))
        form_layout.addWidget(self.char_input)
        controls_layout.addLayout(form_layout)

        self.save_button = QPushButton('Save Config', self)
        self.save_button.clicked.connect(self.save_config)
        controls_layout.addWidget(self.save_button)

        self.api_keys_button = QPushButton('Modify API Keys', self)
        self.api_keys_button.clicked.connect(self.modify_api_keys)
        controls_layout.addWidget(self.api_keys_button)

        main_layout.addLayout(controls_layout)
        self.setLayout(main_layout)

    def update_character_image(self, char_number):
        if char_number in character_images:
            pixmap = QPixmap(character_images[char_number])
            self.image_label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.image_label.setText("No image available")

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
        
        self.update_character_image(character)

    def enable_inputs(self, enabled):
        self.ptt_input.setEnabled(enabled)
        self.lang_input.setEnabled(enabled)
        self.char_input.setEnabled(enabled)
        self.save_button.setEnabled(enabled)
        self.api_keys_button.setEnabled(enabled)

    def modify_api_keys(self):
        api_keys = [
            'DEEPTR_RAPID_API',
            'DEEPGRAM_API_KEY',
            'OPENAI_API_KEY',
            'DEEPL_API_KEY'
            
        ]

        for key in api_keys:
            current_value = os.getenv(key, '')
            new_value, ok = QInputDialog.getText(self, f'Modify {key}', f'Enter new value for {key}:', 
                                                 QLineEdit.Password, current_value)
            if ok and new_value:
                set_key('.env', key, new_value)
                os.environ[key] = new_value

        # Reload environment variables
        load_dotenv()

        # Reload any modules that use these API keys
        importlib.reload(sys.modules['api.deeptranslate'])
        importlib.reload(sys.modules['api.deepgram_transcribe'])
        # Add more module reloads if necessary

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