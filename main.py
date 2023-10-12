from audiogen import VoiceRecorder
from keyboard import wait, is_pressed
from time import sleep
from config import push_to_talk_key
from testingdeeptrans import deeptrans


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
            print(deeptrans("My name is Emu Otori"))
    except KeyboardInterrupt:
        pass

    finally:
        recorder.stream.close()
        recorder.audio.terminate()