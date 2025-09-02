import pyvicon_datastream as pv
from pyvicon_datastream import tools
import time 

VICON_TRACKER_IP = "192.168.1.72"
OBJECT_NAME = "webcam"

mytracker = tools.ObjectTracker(VICON_TRACKER_IP)
while(True):
    position = mytracker.get_position(OBJECT_NAME)
    print(f"Position: {position}")
    time.sleep(0.01)