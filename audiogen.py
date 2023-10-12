import pyaudio
import wave
import array



CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

class VoiceRecorder:
    def __init__(self, push_to_talk_key):
        self.audio = pyaudio.PyAudio()
        self.frames = array.array('h', b'')
        self.push_to_talk_key = push_to_talk_key
        self.recording = False

        self.stream = self.audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
            stream_callback=self.callback
        )

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.frames = array.array('h', b'')
            self.stream.start_stream()
            print("Recording...")

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.stream.stop_stream()
            self.save_to_file()
            print("Recording saved as rec.wav")

    def callback(self, in_data, frame_count, time_info, status):
        if self.recording:
            self.frames.extend(array.array('h', in_data))
        return in_data, pyaudio.paContinue

    def save_to_file(self):
        sound_file = wave.open("rec.wav", "wb")
        sound_file.setnchannels(CHANNELS)
        sound_file.setsampwidth(self.audio.get_sample_size(FORMAT))
        sound_file.setframerate(RATE)
        sound_file.writeframes(self.frames.tobytes())
        sound_file.close()


def voiceplayer():
    p = pyaudio.PyAudio()

    # Open the audio file
    wf = wave.open("./output.wav", 'rb')

    # Open a stream
    stream = p.open(
        format=p.get_format_from_width(wf.getsampwidth()),
        channels=wf.getnchannels(),
        rate=wf.getframerate(),
        output=True,
        #output_device_index=14
    )

    # Read data from the audio file and play it
    data = wf.readframes(1024)
    while data:
        stream.write(data)
        data = wf.readframes(1024)

    # Close the stream and PyAudio
    stream.stop_stream()
    stream.close()
    p.terminate()



# p = pyaudio.PyAudio()

# # Get a list of available audio devices
# devices = []
# for i in range(p.get_device_count()):
#     info = p.get_device_info_by_index(i)
#     devices.append(info['name'])

# # Print the list of available audio devices
# print("Available audio output devices:")
# for i, device in enumerate(devices):
#     print(f"{i}: {device}")

