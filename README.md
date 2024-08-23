# Voxii - voice translating and modding assistant

Voxii is a Python-based project that leverages the ChatGPT API, DeepL API, and VoiceVox to create a voice translation system. The project integrates speech recognition, translation, and voice synthesis to enable users to record spoken phrases in one language, translate them to another language, and then convert the translated text into synthetic character voice using VoiceVox. The Push-to-Talk mechanism is implemented for voice recording.
<br>
#
<img src="https://github.com/user-attachments/assets/9a2ba3f3-9f8b-41da-b32c-a4e0b9ab9fd9" alt="Description of the image" width="300"/>
<br>
## Setup

1. If you don’t have Python installed, [install it from here](https://www.python.org/downloads/).

2. Clone this repository.

3. Navigate into the project directory:

   ```bash
   $ cd Aya_Voxii
   ```

4. Create a new virtual environment:

   ```bash
   $ python -m venv venv
   $ . venv/bin/activate
   ```

5. Install the requirements:

   ```bash
   $ pip install -r requirements.txt
   ```

6. make the environment variables file with your api keys:
   (as in the .env_example file)
   you need the following api keys filled in the env file:
      1. chatgpt api or deepgram api [get deepgram api key](https://deepgram.com/)
      2. deeptranslate api from rapid api [ get deeptranslate api key](https://rapidapi.com/gatzuma/api/deep-translate1)

7. run voice vox in the background  [install it from here](https://voicevox.hiroshiba.jp/)
8. Run the app
   ```bash
   $ python main.py
   ```
