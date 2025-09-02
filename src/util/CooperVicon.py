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
            # self.EnableSegmentData()
            self.enable_segment_data()
            # self.EnableMarkerData()
            self.enable_marker_data()
            # self.EnableUnlabeledMarkerData()
            self.enable_unlabeled_marker_data()
            # self.EnableMarkerRayData()
            # self.EnableDeviceData()
            self.enable_device_data()
            # self.EnableCentroidData()
            # # Report whether the data types have been enabled
            # print( 'Segments', self.IsSegmentDataEnabled() )
            # print( 'Markers', self.IsMarkerDataEnabled() )
            # print( 'Unlabeled Markers', self.IsUnlabeledMarkerDataEnabled() )
            # print( 'Marker Rays', self.IsMarkerRayDataEnabled() )
            # print( 'Devices', self.IsDeviceDataEnabled() )
            # print( 'Centroids', self.IsCentroidDataEnabled() )
        
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

    # def getObjectsData(self):
    #     HasFrame = False
    #     while not HasFrame:
    #         try:
    #             self.GetFrame()
    #             HasFrame = True
    #         except DataStreamException as e:
    #             self.GetFrame()
        
    #     self.SetStreamMode( Client.StreamMode.EClientPull )
    #     print( 'Get Frame Pull', self.GetFrame(), self.GetFrameNumber() )


    #     subjectNames = self.GetSubjectNames()
    #     for subjectName in subjectNames:
    #         print( subjectName )
    #         segmentNames = self.GetSegmentNames( subjectName )
    #         for segmentName in segmentNames:
    #             segmentChildren = self.GetSegmentChildren( subjectName, segmentName )
    #             for child in segmentChildren:
    #                 try:
    #                     print( child, 'has parent', self.GetSegmentParentName( subjectName, segmentName ) )
    #                 except DataStreamException as e:
    #                     print( 'Error getting parent segment', e )
    #             print( segmentName, 'has static translation', self.GetSegmentStaticTranslation( subjectName, segmentName ) )
    #             print( segmentName, 'has static rotation( helical )', self.GetSegmentStaticRotationHelical( subjectName, segmentName ) )               
    #             print( segmentName, 'has static rotation( EulerXYZ )', self.GetSegmentStaticRotationEulerXYZ( subjectName, segmentName ) )              
    #             print( segmentName, 'has static rotation( Quaternion )', self.GetSegmentStaticRotationQuaternion( subjectName, segmentName ) )               
    #             print( segmentName, 'has static rotation( Matrix )', self.GetSegmentStaticRotationMatrix( subjectName, segmentName ) )
    #             try:
    #                 print( segmentName, 'has static scale', self.GetSegmentStaticScale( subjectName, segmentName ) )
    #             except DataStreamException as e:
    #                 print( 'Scale Error', e )               
    #             print( segmentName, 'has global translation', self.GetSegmentGlobalTranslation( subjectName, segmentName ) )
    #             print( segmentName, 'has global rotation( helical )', self.GetSegmentGlobalRotationHelical( subjectName, segmentName ) )               
    #             print( segmentName, 'has global rotation( EulerXYZ )', self.GetSegmentGlobalRotationEulerXYZ( subjectName, segmentName ) )               
    #             print( segmentName, 'has global rotation( Quaternion )', self.GetSegmentGlobalRotationQuaternion( subjectName, segmentName ) )               
    #             print( segmentName, 'has global rotation( Matrix )', self.GetSegmentGlobalRotationMatrix( subjectName, segmentName ) )
    #             print( segmentName, 'has local translation', self.GetSegmentLocalTranslation( subjectName, segmentName ) )
    #             print( segmentName, 'has local rotation( helical )', self.GetSegmentLocalRotationHelical( subjectName, segmentName ) )               
    #             print( segmentName, 'has local rotation( EulerXYZ )', self.GetSegmentLocalRotationEulerXYZ( subjectName, segmentName ) )               
    #             print( segmentName, 'has local rotation( Quaternion )', self.GetSegmentLocalRotationQuaternion( subjectName, segmentName ) )               
    #             print( segmentName, 'has local rotation( Matrix )', self.GetSegmentLocalRotationMatrix( subjectName, segmentName ) )
    #         try:
    #             print( 'Object Quality', self.GetObjectQuality( subjectName ) )
    #         except ViconDataStream.DataStreamException as e:
    #                 print( 'Not present', e )

    #         markerNames = self.GetMarkerNames( subjectName )
    #         for markerName, parentSegment in markerNames:
    #             print( markerName, 'has parent segment', parentSegment, 'position', self.GetMarkerGlobalTranslation( subjectName, markerName ) )
    #             rayAssignments = self.GetMarkerRayAssignments( subjectName, markerName )
    #             if len( rayAssignments ) == 0:
    #                 print( 'No ray assignments for', markerName )
    #             else:
    #                 for cameraId, centroidIndex in rayAssignments:
    #                     print( 'Ray from', cameraId, 'centroid', centroidIndex )

    # def getObjectNames(self):
    #     HasFrame = False
    #     while not HasFrame:
    #         try:
    #             self.GetFrame()
    #             HasFrame = True
    #         except DataStreamException as e:
    #             self.GetFrame()
        
    #     self.SetStreamMode( Client.StreamMode.EClientPull )
    #     print( 'Get Frame Pull', self.GetFrame(), self.GetFrameNumber() )


    #     self.objects = self.GetSubjectNames()
    #     print("Found following objects: ", self.objects)
    #     self.segments = self.GetSegmentNames(self.objects[0])
    #     print("Found following segments: ", self.segments)
    
    # def getFrame(self):
    #     HasFrame = False
    #     while not HasFrame:
    #         try:
    #             self.GetFrame()
    #             HasFrame = True
    #         except DataStreamException as e:
    #             self.GetFrame()
                
    # def getObjectGlobalState(self, subjectName=''):
    #     segmentName = subjectName
    #     translation = self.GetSegmentGlobalTranslation( subjectName, segmentName )
    #     quaternion = self.GetSegmentGlobalRotationQuaternion( subjectName, segmentName )
    #     # time = self.GetTimecode(subjectName, segmentName)
    #     state = State(translation[0], quaternion[0])
    #     return state

    #     # print( segmentName, 'has global translation', self.GetSegmentGlobalTranslation( subjectName, segmentName ) )
    #     # print( segmentName, 'has global rotation( helical )', self.GetSegmentGlobalRotationHelical( subjectName, segmentName ) )               
    #     # print( segmentName, 'has global rotation( EulerXYZ )', self.GetSegmentGlobalRotationEulerXYZ( subjectName, segmentName ) )               
    #     # print( segmentName, 'has global rotation( Quaternion )', self.GetSegmentGlobalRotationQuaternion( subjectName, segmentName ) )               
    #     # print( segmentName, 'has global rotation( Matrix )', self.GetSegmentGlobalRotationMatrix( subjectName, segmentName ) )
    #     # print( segmentName, 'has local translation', self.GetSegmentLocalTranslation( subjectName, segmentName ) )
    #     # print( segmentName, 'has local rotation( helical )', self.GetSegmentLocalRotationHelical( subjectName, segmentName ) )               
    #     # print( segmentName, 'has local rotation( EulerXYZ )', self.GetSegmentLocalRotationEulerXYZ( subjectName, segmentName ) )               
    #     # print( segmentName, 'has local rotation( Quaternion )', self.GetSegmentLocalRotationQuaternion( subjectName, segmentName ) )               
    #     # print( segmentName, 'has local rotation( Matrix )', self.GetSegmentLocalRotationMatrix( subjectName, segmentName ) )

def main():
    vicon = CooperVicon()

if __name__ == "__main__":
    main()