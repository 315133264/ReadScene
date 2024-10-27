import cv2
import logging

from devices.events import *

class Camera:
    def __init__(self) -> None:
        self._camera = cv2.VideoCapture(0)

    def show(self):
        while not end_event.is_set():
            self._ret, self._frame = self._camera.read()
            if self._ret:
                cv2.imshow('Camera Feed', self._frame)
            else:
                logging.info("无法接收帧")
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                start_capturing_event.clear()
                end_event.set()
                break
            if cv2.waitKey(1) & 0xFF == ord('c'):
                start_capturing_event.set()
            if cv2.waitKey(1) & 0xFF == ord('s'):
                start_capturing_event.clear()

    def read(self):
        return self._ret, self._frame

    def releas(self):
        end_event.set()
        self._camera.release()
        cv2.destroyAllWindows()