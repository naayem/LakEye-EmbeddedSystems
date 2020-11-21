import cv2
from threading import Thread


class CamStream:
    def __init__(self, src=0):
        self.cam = cv2.VideoCapture(src)
        self.grabbed, self.frame = None, None

    def start(self):
        """start the thread to read frames from the video stream"""
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        """keep looping infinitely until the thread is stopped"""
        while True:
            (self.grabbed, self.frame) = self.cam.read()

    def read(self):
        """return the frame most recently read"""
        return self.grabbed, self.frame
