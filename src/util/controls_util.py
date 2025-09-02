class State:
    def __init__(self, translation=[0,0,0], quaternion=[0,0,0,1]):
        self.translation = translation
        self.quaternion = quaternion
    def pretty_print(self):
        print("Translation: ", self.translation)
        print("Quaternion: ", self.quaternion)

class Trajectory:
    def __init__(self):
        pass