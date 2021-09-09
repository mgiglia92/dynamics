from VideoStream import VideoStream, CalibrationParameters
import cv2
import numpy as np
import glob
import time
import pickle

stream = VideoStream(0)
stream.start()
time.sleep(2)

params = pickle.load("calib_params.txt")

