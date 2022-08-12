from VideoStream import VideoStream
import cv2
import numpy as np
import glob
import time
import pickle

stream = VideoStream(1)
stream.start()
time.sleep(2)

images=[]

for i in range(0, 10):
    input('Press Enter to take new pic: ' + str(i) + '/10')
    images.append(stream.frame)

with open("images.txt", "wb") as fp:
    pickle.dump(images, fp)