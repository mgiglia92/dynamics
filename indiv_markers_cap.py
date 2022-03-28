from CooperVicon import CooperVicon
from data_util import RelativeMotionData
from VideoStream import VideoStream, VideoStreamCalibrated
import matplotlib.pyplot as plt
import time
import numpy as np
import scipy.stats as stats
import cv2
from threading import Thread
import csv
import os

data = RelativeMotionData()

vicon_obj = CooperVicon()
# vicon_obj.getObjectsData()
# vicon_obj.printObjects()
vicon_obj.getObjectNames()

#Setup a figure
# plt.figure(1)


if __name__ == "__main__":
    stream = VideoStream(0)
    stream.start()
    time.sleep(2)
    dts=[]
    frame_duration = 1/20 # 1/framerate
    collection_duration = 10 # #of seconds to record data
    i=0

    # Record frames from video stream and pull vicon data
    while i < (collection_duration/frame_duration):
        try:
            t1 = time.time()
            frame = stream.get_frame()
            vicon_obj.getFrame()
            # markers = vicon_obj.getObjectGlobalState('rc_car')
            markers = vicon_obj.GetUnlabeledMarkers()
            ml = vicon_obj.GetLabeledMarkers()

            # append data
            # data.append(frame_duration, cam_state, obj_state, frame)
            t2 = time.time()
            dt = t2-t1
        except Exception as e:  
            print(e)
        
        # Pause desired amount of time
        while(time.time() - t1) <= frame_duration:
            pass
        print(time.time()-t1)

        i += 1

    print("Done recording, saving data.")

    file_prefix = input("Please enter the filename you would like to use: ")
    path = file_prefix + '/' + file_prefix
    # Attempt to make directory
    os.mkdir(file_prefix)
    # Save video
    writer = cv2.VideoWriter(filename=os.path.join(file_prefix, 'video.mp4'), apiPreference=cv2.CAP_FFMPEG, fourcc=cv2.VideoWriter_fourcc(*'mp4v'), \
                    fps=1/frame_duration, frameSize=(640,480), params=None)
    for i in range(0, len(data.frames)):
        writer.write(data.frames[i])
    writer.release()
    print("Video saved as relative_motion.mp4")
    print("Video has " + str(len(data.frames)) + " frames")
    # Save translation/quaternion data
    fields = ['time', 'cam_x', 'cam_y', 'cam_z', 'obj_x', 'obj_y', 'obj_z', \
                'cam_i', 'cam_j', 'cam_k', 'cam_w', 'obj_i', 'obj_j', 'obj_k', 'obj_w']

    filename = path + ".csv"

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
