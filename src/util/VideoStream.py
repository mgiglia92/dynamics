#!/usr/bin/env python2
import cv2
from threading import Thread
import pickle

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

class VideoStreamCalibrated(Thread):
    def __init__(self, input_num=0):
        Thread.__init__(self, target=self.stream, daemon=True)
        self.cap = cv2.VideoCapture(input_num)
        self.frame=[]
        if(self.cap.isOpened() == False):
            print("Failed to open webcam")
        self.width = self.cap.get(3)
        self.height = self.cap.get(4)
        self.fps = self.cap.get(5)
        self.distortion_params = pickle.load(open("calib_params.txt", "rb"))

    def stream(self):
        while(1):
            ret, self.frame = self.cap.read()
            h,  w = self.frame.shape[:2]
            newcameramtx, roi = cv2.getOptimalNewCameraMatrix(self.distortion_params.mtx, self.distortion_params.dist, (w,h), 1, (w,h))
            # undistort
            dst = cv2.undistort(self.frame, self.distortion_params.mtx, self.distortion_params.dist, None, newcameramtx)
            # crop the image
            x, y, w, h = roi
            dst = dst[y:y+h, x:x+w]
            cv2.imshow('Original', self.frame)
            # cv2.imshow('Undistored', dst)
            # cv2.imshow('overlay', cv2.addWeighted(self.frame, .5, dst, 0.5, 0.0))
            if cv2.waitKey(1) & 0xFF == ord('q'):
                # After the loop release the cap object
                self.cap.release()
                # Destroy all the windows
                cv2.destroyAllWindows()
    
    def get_frame(self):
        return self.frame

class CalibrationParameters:
    def __init__(self, ret, mtx, dist, rvecs, tvecs):
        self.ret = ret
        self.mtx = mtx
        self.dist = dist
        self.rvecs = rvecs
        self.tvecs = tvecs

if __name__ == "__main__":
    stream = VideoStreamCalibrated(1)
    stream.start()
    while(1): pass