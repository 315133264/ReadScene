import time
import os
import threading
import signal
import shutil
import logging

from config.configuration import *

from handlers.pic_handler import PicHandler
from devices.camera.camera import Camera
from devices.events import *

def schedule_photos(interval_seconds, pichandler: PicHandler):
    while not end_event.is_set():
        if start_capturing_event.is_set():
            pichandler.take_photo()
        time.sleep(interval_seconds)

def signal_handler(signum, frame):
    end_event.set()
    #sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)  # Ctrl+C
signal.signal(signal.SIGTERM, signal_handler) # Terminate信号

def main():
    try:
        if not os.path.exists(PHOTO_DIR):
            os.makedirs(PHOTO_DIR)
        if not os.path.exists(AUDIO_DIR):
            os.makedirs(AUDIO_DIR)
        
        camera = Camera()
        pichandler = PicHandler(camera)
        capture_thread = threading.Thread(target=schedule_photos, args=[INTERVAL_SECONDS, pichandler], daemon=True)
        capture_thread.start()

        camera.show()

        while not end_event.is_set():
            time.sleep(1)
        
    except Exception as e:
        logging.error(str(e))
    finally:
        if os.path.exists(PHOTO_DIR):
            shutil.rmtree(PHOTO_DIR)
        if os.path.exists(AUDIO_DIR):
            shutil.rmtree(AUDIO_DIR)
        camera.releas()
        capture_thread.join()


if __name__ == "__main__":
    main()
