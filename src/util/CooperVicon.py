from vicon_dssdk.ViconDataStream import Client, DataStreamException
from util.controls_util import State

class CooperVicon(Client):
    def __init__(self, ip='199.98.17.181'):
        super().__init__()
        try:
            self.Connect(ip)
            # Check the version
            print( 'Version', self.GetVersion() )

            # Check setting the buffer size works
            self.SetBufferSize( 1 )

            #Enable all the data types
            self.EnableSegmentData()
            self.EnableMarkerData()
            self.EnableUnlabeledMarkerData()
            self.EnableMarkerRayData()
            self.EnableDeviceData()
            self.EnableCentroidData()
            # Report whether the data types have been enabled
            print( 'Segments', self.IsSegmentDataEnabled() )
            print( 'Markers', self.IsMarkerDataEnabled() )
            print( 'Unlabeled Markers', self.IsUnlabeledMarkerDataEnabled() )
            print( 'Marker Rays', self.IsMarkerRayDataEnabled() )
            print( 'Devices', self.IsDeviceDataEnabled() )
            print( 'Centroids', self.IsCentroidDataEnabled() )
        
        except DataStreamException as e:
            print(e)
    def getObjectsData(self):
        HasFrame = False
        while not HasFrame:
            try:
                self.GetFrame()
                HasFrame = True
            except DataStreamException as e:
                self.GetFrame()
        
        self.SetStreamMode( Client.StreamMode.EClientPull )
        print( 'Get Frame Pull', self.GetFrame(), self.GetFrameNumber() )


        subjectNames = self.GetSubjectNames()
        for subjectName in subjectNames:
            print( subjectName )
            segmentNames = self.GetSegmentNames( subjectName )
            for segmentName in segmentNames:
                segmentChildren = self.GetSegmentChildren( subjectName, segmentName )
                for child in segmentChildren:
                    try:
                        print( child, 'has parent', self.GetSegmentParentName( subjectName, segmentName ) )
                    except DataStreamException as e:
                        print( 'Error getting parent segment', e )
                print( segmentName, 'has static translation', self.GetSegmentStaticTranslation( subjectName, segmentName ) )
                print( segmentName, 'has static rotation( helical )', self.GetSegmentStaticRotationHelical( subjectName, segmentName ) )               
                print( segmentName, 'has static rotation( EulerXYZ )', self.GetSegmentStaticRotationEulerXYZ( subjectName, segmentName ) )              
                print( segmentName, 'has static rotation( Quaternion )', self.GetSegmentStaticRotationQuaternion( subjectName, segmentName ) )               
                print( segmentName, 'has static rotation( Matrix )', self.GetSegmentStaticRotationMatrix( subjectName, segmentName ) )
                try:
                    print( segmentName, 'has static scale', self.GetSegmentStaticScale( subjectName, segmentName ) )
                except DataStreamException as e:
                    print( 'Scale Error', e )               
                print( segmentName, 'has global translation', self.GetSegmentGlobalTranslation( subjectName, segmentName ) )
                print( segmentName, 'has global rotation( helical )', self.GetSegmentGlobalRotationHelical( subjectName, segmentName ) )               
                print( segmentName, 'has global rotation( EulerXYZ )', self.GetSegmentGlobalRotationEulerXYZ( subjectName, segmentName ) )               
                print( segmentName, 'has global rotation( Quaternion )', self.GetSegmentGlobalRotationQuaternion( subjectName, segmentName ) )               
                print( segmentName, 'has global rotation( Matrix )', self.GetSegmentGlobalRotationMatrix( subjectName, segmentName ) )
                print( segmentName, 'has local translation', self.GetSegmentLocalTranslation( subjectName, segmentName ) )
                print( segmentName, 'has local rotation( helical )', self.GetSegmentLocalRotationHelical( subjectName, segmentName ) )               
                print( segmentName, 'has local rotation( EulerXYZ )', self.GetSegmentLocalRotationEulerXYZ( subjectName, segmentName ) )               
                print( segmentName, 'has local rotation( Quaternion )', self.GetSegmentLocalRotationQuaternion( subjectName, segmentName ) )               
                print( segmentName, 'has local rotation( Matrix )', self.GetSegmentLocalRotationMatrix( subjectName, segmentName ) )
            try:
                print( 'Object Quality', self.GetObjectQuality( subjectName ) )
            except ViconDataStream.DataStreamException as e:
                    print( 'Not present', e )

            markerNames = self.GetMarkerNames( subjectName )
            for markerName, parentSegment in markerNames:
                print( markerName, 'has parent segment', parentSegment, 'position', self.GetMarkerGlobalTranslation( subjectName, markerName ) )
                rayAssignments = self.GetMarkerRayAssignments( subjectName, markerName )
                if len( rayAssignments ) == 0:
                    print( 'No ray assignments for', markerName )
                else:
                    for cameraId, centroidIndex in rayAssignments:
                        print( 'Ray from', cameraId, 'centroid', centroidIndex )

    def getObjectNames(self):
        HasFrame = False
        while not HasFrame:
            try:
                self.GetFrame()
                HasFrame = True
            except DataStreamException as e:
                self.GetFrame()
        
        self.SetStreamMode( Client.StreamMode.EClientPull )
        print( 'Get Frame Pull', self.GetFrame(), self.GetFrameNumber() )


        self.objects = self.GetSubjectNames()
        print("Found following objects: ", self.objects)
        self.segments = self.GetSegmentNames(self.objects[0])
        print("Found following segments: ", self.segments)
    
    def getFrame(self):
        HasFrame = False
        while not HasFrame:
            try:
                self.GetFrame()
                HasFrame = True
            except DataStreamException as e:
                self.GetFrame()
                
    def getObjectGlobalState(self, subjectName=''):
        segmentName = subjectName
        translation = self.GetSegmentGlobalTranslation( subjectName, segmentName )
        quaternion = self.GetSegmentGlobalRotationQuaternion( subjectName, segmentName )
        # time = self.GetTimecode(subjectName, segmentName)
        state = State(translation[0], quaternion[0])
        return state

        # print( segmentName, 'has global translation', self.GetSegmentGlobalTranslation( subjectName, segmentName ) )
        # print( segmentName, 'has global rotation( helical )', self.GetSegmentGlobalRotationHelical( subjectName, segmentName ) )               
        # print( segmentName, 'has global rotation( EulerXYZ )', self.GetSegmentGlobalRotationEulerXYZ( subjectName, segmentName ) )               
        # print( segmentName, 'has global rotation( Quaternion )', self.GetSegmentGlobalRotationQuaternion( subjectName, segmentName ) )               
        # print( segmentName, 'has global rotation( Matrix )', self.GetSegmentGlobalRotationMatrix( subjectName, segmentName ) )
        # print( segmentName, 'has local translation', self.GetSegmentLocalTranslation( subjectName, segmentName ) )
        # print( segmentName, 'has local rotation( helical )', self.GetSegmentLocalRotationHelical( subjectName, segmentName ) )               
        # print( segmentName, 'has local rotation( EulerXYZ )', self.GetSegmentLocalRotationEulerXYZ( subjectName, segmentName ) )               
        # print( segmentName, 'has local rotation( Quaternion )', self.GetSegmentLocalRotationQuaternion( subjectName, segmentName ) )               
        # print( segmentName, 'has local rotation( Matrix )', self.GetSegmentLocalRotationMatrix( subjectName, segmentName ) )