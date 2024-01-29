from dotenv import load_dotenv
import os
import requests

# Load variables from the .env file
load_dotenv()

# Access the variables
elLab = os.getenv("11LAB")
voice_id = 'TxGEqnHWrfWFTfGW9XjX'

def text_to_speech(text):
    url = f'https://api.elevenlabs.io/v1/text-to-speech/{voice_id}'
    headers = {
        'Accept': 'audio/mpeg',
        'xi-api-key': elLab,
        'Content-Type': 'application/json'
    }
    data = {
        'text': text,
        'model_id': 'eleven_monolingual_v1',
        'voice_settings': {
            'stability': 0.6,
            'similarity_boost': 0.85
        }
    }
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        with open('output.mp3', 'wb') as f:
            f.write(response.content)
        print("Audio was recorded")
    else:
        print('Error:', response.text)