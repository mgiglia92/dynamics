#!/usr/bin/env python2
import cv2
from threading import Thread


class VideoStream(Thread):
    def __init__(self, input_num=0):
        Thread.__init__(self, target=self.stream, daemon=True)
        self.cap = cv2.VideoCapture(input_num)
        self.frame=[]
        if(self.cap.isOpened() == False):
            print("Failed to open webcam")
        self.width = self.cap.get(3)
        self.height = self.cap.get(4)
        self.fps = self.cap.get(5)

    def stream(self):
        while(1):
            ret, self.frame = self.cap.read()
            cv2.imshow('Frame', self.frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                # After the loop release the cap object
                self.cap.release()
                # Destroy all the windows
                cv2.destroyAllWindows()
    
    def get_frame(self):
        return self.frame

