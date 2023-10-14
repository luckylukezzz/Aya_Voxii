from deepgram import Deepgram

DEEPGRAM_API_KEY=''
deepgram = Deepgram(DEEPGRAM_API_KEY)

async def transcribe_audio():

    audio=open("rec.wav", "rb")
    # Set the source
    source = {
      'buffer': audio,
      'mimetype': "wav"
    }
    try:
        response = await deepgram.transcription.prerecorded(source, {'punctuate': True})
        print(response['results']['channels'][0]['alternatives'][0]['transcript'])
    except Exception as e:
        print(f"An error occurred: {e}")
