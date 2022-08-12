from CooperVicon import CooperVicon
from data_util import RelativeMotionData
from VideoStream import VideoStream
import matplotlib.pyplot as plt
import time
import numpy as np
import scipy.stats as stats
import cv2
from threading import Thread


if __name__ == "__main__":
    stream = VideoStream(1+cv2.CAP_DSHOW)
    print("Cam exposure: " + str(stream.cap.get(cv2.CAP_PROP_EXPOSURE)))
    stream.cap.set(cv2.CAP_PROP_EXPOSURE, 10)
    print("Cam exposure2: " + str(stream.cap.get(cv2.CAP_PROP_EXPOSURE)))
    stream.cap.set(cv2.CAP_PROP_SETTINGS, 0)
    stream.start()
    time.sleep(2)
    dts=[]
    frame_duration = 1/10 # 1/framerate
    i=0

    # Record frames from video stream and pull vicon data
    while 1:
        t1 = time.time()
        frame = stream.get_frame()
        
        t2 = time.time()
        dt = t2-t1
        
        # Pause desired amount of time
        if((t2-t1 < frame_duration)):
            time.sleep(frame_duration - (t2-t1))
            print(time.time() - t1)

        i += 1

    print("Done recording, saving data.")
    # Save video
    writer = cv2.VideoWriter(filename='relative_motion.mp4', apiPreference=cv2.CAP_FFMPEG, fourcc=cv2.VideoWriter_fourcc(*'mp4v'), \
                    fps=(1/frame_duration), frameSize=(640,480), params=None)
    for i in range(0, len(data.frames)):
        writer.write(data.frames[i])
    writer.release()
    print("Video saved as relative_motion.mp4")

    # Save translation/quaternion data
    fields = ['time', 'cam_x', 'cam_y', 'cam_z', 'obj_x', 'obj_y', 'obj_z', \
                'cam_i', 'cam_j', 'cam_k', 'cam_w', 'obj_i', 'obj_j', 'obj_k', 'obj_w']

    filename = "cam_obj_data.csv"

    csvfile = open(filename, 'w', newline="")
    csvwriter = csv.writer(csvfile, delimiter=',')
    csvwriter.writerow(fields)

    for i in range(0, len(data.camera_state)):
        row = []
        row.append(data.time[i])
        for a in data.camera_state[i].translation: row.append(a)
        for a in data.object_state[i].translation: row.append(a)
        for a in data.camera_state[i].quaternion: row.append(a)
        for a in data.object_state[i].quaternion: row.append(a)
        csvwriter.writerow(row)

    print("CSV Data saved")