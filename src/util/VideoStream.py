#!/usr/bin/env python2
import cv2
from threading import Thread
import pickle
import traceback

class VideoStream(Thread):
    def __init__(self, input_num=0):
        Thread.__init__(self, target=self.stream, daemon=True)
        try:
            self.cap = cv2.VideoCapture(input_num)
            self.frame=[]
            if(self.cap.isOpened() == False):
                print("Failed to open webcam")
            # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
            # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
            self.exposure   = 10.
            self.brightness = 128.
            self.contrast   = 32.
            self.saturation = 32.
            self.cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
            self.cap.set(cv2.CAP_PROP_EXPOSURE, self.exposure)
            self.cap.set(cv2.CAP_PROP_BRIGHTNESS, self.brightness)
            self.cap.set(cv2.CAP_PROP_CONTRAST, self.contrast)
            self.cap.set(cv2.CAP_PROP_SATURATION, self.saturation)
            self.width = self.cap.get(3)
            self.height = self.cap.get(4)
            self.fps = self.cap.get(5)
            # self.exposure   = self.cap.get(cv2.CAP_PROP_EXPOSURE)
            # self.brightness = self.cap.get(cv2.CAP_PROP_BRIGHTNESS)
            # self.contrast   = self.cap.get(cv2.CAP_PROP_CONTRAST)
            # self.saturation = self.cap.get(cv2.CAP_PROP_SATURATION)
            print(f"w:{self.width} h:{self.height} fps:{self.fps}, exposure: {self.cap.get(cv2.CAP_PROP_EXPOSURE)}" +
                   f" brightness: {self.brightness} contrast: {self.contrast} saturation: {self.saturation}")

        except Exception as e:
            print(e)
            traceback.print_exc()

    def update_params(self, val):
        exp = cv2.getTrackbarPos('Exposure', 'Frame')
        bri = cv2.getTrackbarPos('Brightness', 'Frame')
        con = cv2.getTrackbarPos('Contrast', 'Frame')
        sat = cv2.getTrackbarPos('Saturation', 'Frame')
        self.cap.set(cv2.CAP_PROP_EXPOSURE,     exp)
        self.cap.set(cv2.CAP_PROP_BRIGHTNESS,   bri)
        self.cap.set(cv2.CAP_PROP_CONTRAST,     con)
        self.cap.set(cv2.CAP_PROP_SATURATION,   sat)

    def stream(self):
        cv2.namedWindow('Frame')
        cv2.createTrackbar('Exposure', 'Frame',    int(self.exposure),     255, self.update_params)
        cv2.createTrackbar('Brightness', 'Frame',   int(self.brightness),   255, self.update_params)
        cv2.createTrackbar('Contrast', 'Frame',     int(self.contrast),     255, self.update_params)
        cv2.createTrackbar('Saturation', 'Frame',   int(self.saturation),   255, self.update_params)

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
        self.distortion_params = pickle.load(open("src/util/calib_params.txt", "rb"))

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
    stream = VideoStream(0)
    stream.start()
    while(1): pass