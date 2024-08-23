from aiohttp import ClientSession
import asyncio

def voiceoutput(jptext,speaker_id=0):
    async def get_audio_file(japanese_text, speaker):
        async with ClientSession() as session:
            # Step 1: Send a POST request to the audio_query endpoint with Japanese text and speaker information
            async with session.post(f"http://localhost:50021/audio_query?text={japanese_text}&speaker={speaker}") as query_response:
                # Step 2: Read the JSON response from the audio_query endpoint
                query_json = await query_response.text()
                # Step 3: Send a POST request to the synthesis endpoint with speaker information and the JSON response from the previous step
                async with session.post(f"http://localhost:50021/synthesis?speaker={speaker}", data=query_json, headers={'Content-Type': 'application/json'}) as audio_response:
                    # Step 4: Create or overwrite an audio file and write the binary content of the audio response to the file
                    with open('./output.wav', 'wb') as audio_file:
                        audio_file.write(await audio_response.read())

    # Run the event loop
    asyncio.run(get_audio_file(jptext, 0))
    print("voice generated")