from audiogen import VoiceRecorder,voiceplayer
from keyboard import wait, is_pressed
from time import sleep
from config import push_to_talk_key
from testingdeeptrans import deeptrans
from openapi import transcribe_openai
from voicevoxRequests import voiceoutput

if __name__ == "__main__":
    recorder = VoiceRecorder(push_to_talk_key)
    try:
        while True:
            wait(push_to_talk_key)
            recorder.start_recording()

            # Wait until the key is released
            while is_pressed(push_to_talk_key):
                sleep(0.1)

            recorder.stop_recording()
            engtext = transcribe_openai()
            print(engtext)
            jptext= (deeptrans(engtext))
            print(jptext)
            voiceoutput(jptext,6)
            voiceplayer()
    except KeyboardInterrupt:
        pass

    finally:
        recorder.stream.close()
        recorder.audio.terminate()