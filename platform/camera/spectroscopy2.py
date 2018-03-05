import cv2
import numpy as np
from time import gmtime,strftime
import time, math, os, csv
import threading

start_time = 0
elapsed_time = 0
SLEEP_TIME = 0.1

class VideoCapture(threading.Thread):
    """
    This class query frames as fast a possible for other programs to use
    """
    def __init__(self, device=0, frame_size=(640, 480)):
        threading.Thread.__init__(self)
        self.daemon = True
        self.interrupted = threading.Lock()
        self.lock = threading.Lock()

        self.device = device
        self.frame_size = frame_size

        self.open()

        self.video_capture.set(cv2.cv.CV_CAP_PROP_BRIGHTNESS, 0)
        self.video_capture.set(cv2.cv.CV_CAP_PROP_CONTRAST, 0.152941182256)
        self.video_capture.set(cv2.cv.CV_CAP_PROP_GAIN, 0)
        self.video_capture.set(cv2.cv.CV_CAP_PROP_EXPOSURE, 0.470588237047)

        self.start()
        self.wait_until_ready()

    def open(self):
        self.video_capture = cv2.VideoCapture(self.device)
        self.video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, self.frame_size[0])
        self.video_capture.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, self.frame_size[1])

    def close(self):
        if hasattr(self, "video_capture"):
            self.video_capture.release()

    def __del__(self):
        self.close()

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def stop(self):
        self.interrupted.release()

    def run(self):
        self.interrupted.acquire()
        while self.interrupted.locked():
            ret, frame = self.video_capture.read()
            if ret:
                self.lock.acquire()
                self.frame = frame
                self.lock.release()
        self.close()

    def wait_until_ready(self):
        while not hasattr(self, 'frame'):
            time.sleep(SLEEP_TIME)

    def get_last_frame(self):
        self.lock.acquire()
        frame = self.frame.copy()
        self.lock.release()
        return frame

class VideoRecorder(object):

    def __init__(self, device, frame_size=(640, 480)):
        #self.logger = create_logger(self.__class__.__name__)

        self.device = device
        self.frame_size = frame_size
        self.video_capture = VideoCapture(self.device, self.frame_size)

    def close(self):
        self.video_capture.stop()
        self.video_capture.join()

    def save_frame(self,filename):
        frame = self.video_capture.get_last_frame()
        cv2.imwrite(filename, frame)
        print ("Frame saved")

    def get_video(self):
        print (" Press q to quit at any time")
        while True:
            # Capture frame-by-frame
            frame = self.video_capture.get_last_frame()
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break