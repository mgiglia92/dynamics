import numpy as np
import csv
import matplotlib.pyplot as plt

tracker_data = np.genfromtxt('tracker_data.txt', delimiter=',', skip_header=2)
tracker_data = np.nan_to_num(tracker_data, nan=0.0)
tracker_data=tracker_data*-1000 # Convert m to mm and flip x axis
vicon_data = np.genfromtxt('cam_obj_data.csv', delimiter=',', skip_header=1)
all_data = np.concatenate((vicon_data, tracker_data), axis=1)
print(all_data)

# Separate data
time = all_data[:,15]
pencil_vicon = all_data[:, 4]
pencil_tracker = all_data[:,16]  #Convert from m to mm
cam_pos = all_data[:, 1]
pencil_fixed = cam_pos+pencil_tracker

# Plot data
plt.figure(1)
plt.plot(time, pencil_vicon, 'r.', label='pencil_vicon')
plt.plot(time, pencil_tracker, 'b.', label='pencil_tracker')
plt.plot(time, pencil_fixed, 'g.', label='pencil_fixed')
plt.plot(time, cam_pos, 'c.', label='cam_pos')

plt.legend(loc='lower right')
plt.show()