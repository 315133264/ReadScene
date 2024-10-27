import openai
from playsound import playsound
from config.configuration import *
import time
import os

class TTSHandler:
    def __init__(self) -> None:
        pass

    def convert(self, s: str):
        if(TTS_MODEL_TYPE == MODEL.openai):
            self.use_openai(s)
        elif(TTS_MODEL_TYPE == MODEL.llama):
            self.use_ollama(s)

    def use_openai(self, s: str):
        openai.api_key = OPENAI_API_KEY
        cn_resp = openai.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": f"""translate the given text into chinese. text:{s}"""}]
        )
        cn_input = cn_resp.choices[0].message.content
        response = openai.audio.speech.create(
            model="tts-1",
            voice='nova',
            response_format='mp3',
            input=cn_input
        )

        timestamp = time.strftime('%Y%m%d_%H%M%S')
        path = os.path.join('audios', f'audio_{timestamp}.mp3')
        response.write_to_file(path)

        playsound(path)

    def use_ollama(self, s: str):
        pass