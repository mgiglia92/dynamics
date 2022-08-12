from controls_util import State

class RelativeMotionData:
    def __init__(self):
        self.time = []
        self.camera_state = []
        self.object_state = []
        self.frames = []
    def append(self, time: float, cam_state: State, obj_state: State, frame):
        self.camera_state.append(cam_state)
        self.object_state.append(obj_state)
        self.frames.append(frame)
        self.time.append(time)
    