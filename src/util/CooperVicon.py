# from vicon_dssdk.ViconDataStream import Client, DataStreamException
import pyvicon_datastream as pv
# from pyvicon_datastream import tools 
from pyvicon_datastream import PyViconDatastream
from pyvicon_datastream.tools import ObjectTracker
from util.controls_util import State

class CooperVicon(PyViconDatastream):
    def __init__(self, ip='192.168.1.72'):
        super().__init__()
        try:
            ret = self.connect(ip)
            self.tracker = ObjectTracker(ip)
            # Check the version
            
            # print( 'Version', self.GetVersion() )

            # # Check setting the buffer size works
            # self.SetBufferSize( 1 )
            self.set_buffer_size(1)

            # #Enable all the data types
            self.enable_segment_data()
            self.enable_marker_data()
            self.enable_unlabeled_marker_data()
            self.enable_device_data()
        
        except Exception as e:
            print(e)

    def _get_object_state_quaternion(self, name):
        subject_count = self.get_subject_count()
        positions = []
        state = State([],[])
        for subj_idx in range(subject_count):
            subject_name = self.get_subject_name(subj_idx)

            if subject_name != name: #Skip objects we are not interessted in
                continue
            
            segment_count = self.get_segment_count(name)
            for seg_idx in range(segment_count):
                segment_name = self.get_segment_name(subject_name, seg_idx)
                segment_global_translation = self.get_segment_global_translation(subject_name, segment_name)
                segment_local_quaternion   = self.get_segment_global_quaternion(subject_name, segment_name)

                if segment_global_translation is not None and segment_local_quaternion is not None:
                    position_x = segment_global_translation[0]
                    position_y = segment_global_translation[1]
                    position_z = segment_global_translation[2]
                    qx = segment_local_quaternion[0]
                    qy = segment_local_quaternion[1]
                    qz = segment_local_quaternion[2]
                    qw = segment_local_quaternion[3]

                    position_entry = [
                        subject_name, 
                        segment_name, 
                        position_x,
                        position_y,
                        position_z,
                        qx,
                        qy,
                        qz,
                        qw
                    
                    ]
                    state = State(segment_global_translation, segment_local_quaternion)
                    positions.append(position_entry)
        return state
    
    def get_object_state(self, object_name):
        if self.tracker.is_connected == True:
            frame = self.get_frame()
            if frame == pv.Result.Success:
                t     = self.tracker.get_timecode()
                framenumber = self.get_frame_number()
                state    = self._get_object_state_quaternion(object_name)
                return ViconStateData(t, framenumber, state)
        return False
    
class ViconStateData:
    time: float
    framenumber: int
    state: State

    def __init__(self, time, framenumber, state):
        self.time = time
        self.framenumber = framenumber
        self.state = state

def main():
    vicon = CooperVicon()

if __name__ == "__main__":
    main()