from deepgram import Deepgram
from asyncio import run 
DEEPGRAM_API_KEY='aaf11ae92027d33bb893d307bac9619c4a16a825a'
deepgram = Deepgram(DEEPGRAM_API_KEY)

async def transcribe_audio():
    source = {'url': "./rec.wav"}
    try:
        response = await deepgram.transcription.prerecorded(source, {'punctuate': True})
        print(response)
    except Exception as e:
        print(f"An error occurred: {e}")


run(transcribe_audio())
