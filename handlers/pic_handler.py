from handlers.model_handler import ModelHandler
from config.configuration import *
from handlers.tts_handler import TTSHandler

import cv2
import logging
import time
import os

class PicHandler:
    def __init__(self, camera):
        self._model = ModelHandler()
        self._tts_handler = TTSHandler()
        self._files = []
        self._camera = camera

    def take_photo(self):
        timestamp = time.strftime('%Y%m%d_%H%M%S')
        photo_path = os.path.join(PHOTO_DIR, f'photo_{timestamp}.jpg')

        ret, frame = self._camera.read()

        if ret:
            cv2.imwrite(photo_path, frame)
            logging.info(f'Photo saved to {photo_path}')
            result = self.update_pic(photo_path)
            # logging.info(result)
            # if result != 'skip' and TTS_MODEL_TYPE != '':
            #     self._tts_handler.convert(result)
        else:
            logging.info('Failed to capture image')

    def update_pic(self, file_name):
        try:
            self._files.append(file_name)
            if(len(self._files) <= NUM_OF_FILES_TO_BE_SEEN):
                return 'skip'
            else:
                self._files.pop(0)
                return self._model.process(self._files)
        except Exception as e:
            return str(e)