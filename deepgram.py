
import deepgram
import asyncio
dg_client = deepgram.Deepgram({ 
  "api_key": 'aaf11ae92027d33bb893d307bac9619c4a16a825a', 
  "api_url": "http://localhost:8080/v1/listen" 
})
async def transcribe_audio():
    source = {'url': "./rec.wav"}
    try:
        response = await dg_client.transcription.prerecorded(source, {'punctuate': True})
        print(response)
    except Exception as e:
        print(f"An error occurred: {e}")



asyncio.run(transcribe_audio())
print(dir(deepgram))