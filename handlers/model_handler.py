import openai
import base64
import requests
from config.configuration import *

class ModelHandler:
    def __init__(self):
        self._model = IMAGE_MODEL_TYPE
        self._system_prompt = '''You are a very advanced model and your task is to describe the image as precisely as possible. Transcribe any text you see.'''
        self._user_prompt = 'Describe the scene'

    def process(self, files):
        if self._model == MODEL.openai:
            return self.use_openai(files)
        elif self._model == MODEL.llama or self._model == MODEL.llava:
            return self.use_ollama(files)

    def use_openai(self, files):
        openai.api_key = OPENAI_API_KEY
        messages = self.create_msgs(files)
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=messages,
        )

        resp = response.choices[0].message.content

        return resp

    def create_msgs(self, files):
        msgs = [{"role": "system", "content": [self.create_content("text", self._system_prompt)]},
                {"role": "user", "content": [self.create_content("text", self._user_prompt)]}]
        
        for f in files:
            base64_image = self.encode_image(f)
            msgs[1]["content"].append(self.create_content('image_url', {"url": f"data:image/jpeg;base64,{base64_image}"}))

        return msgs
        
    def create_content(self, type, content):
        return {"type":type, type:content}
    
    def encode_image(self, image_path):
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')
        

    def use_ollama(self, files):
        url = OLLAMA_URL

        msgs = self.create_ollama_msgs(files)

        data = {
            "model": str(self._model.name),
            "messages": msgs,
            "stream": "false"
        }

        response = requests.post(url, json=data)
        return response.content
    
    def create_ollama_msgs(self, files):
        msgs = [{"role": "system", "content": self._system_prompt},
                {"role": "user", "content": self._user_prompt, "images":[]}]
        
        for f in files:
            base64_image = self.encode_image(f)
            msgs[1]["images"].append(base64_image)

        return msgs
    
    