import threading
import time
from audiogen import VoiceRecorder, voiceplayer
from keyboard import wait, is_pressed
from time import sleep
from config import push_to_talk_key, character
from deeptranslate import deeptrans
from openapi import transcribe_openai
from voicevoxRequests import voiceoutput
from deepgram_transcribe import deepgram_tc

# Global flag to control the running state
running = True
lock = threading.Lock()

def run():
    global running
    recorder = VoiceRecorder(push_to_talk_key)
    
    try:
        while running:
            wait(push_to_talk_key)
            recorder.start_recording()

            # Wait until the key is released
            while is_pressed(push_to_talk_key):
                sleep(0.1)

            recorder.stop_recording()

            # uncomment these to select the required transcribe api
            engtext = deepgram_tc()
            # engtext = transcribe_openai()

            print(engtext)
            jptext = deeptrans(engtext)
            print(jptext)
            voiceoutput(jptext, character)
            voiceplayer()
    except KeyboardInterrupt:
        pass
    finally:
        recorder.stream.close()
        recorder.audio.terminate()

def stop():
    global running
    with lock:
        running = False
