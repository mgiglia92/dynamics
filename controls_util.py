class State:
    def __init__(self, translation, quaternion):
        self.translation = translation
        self.quaternion = quaternion
    def pretty_print(self):
        print("Translation: ", self.translation)
        print("Quaternion: ", self.quaternion)

class Trajectory:
    def __init__(self):
        pass