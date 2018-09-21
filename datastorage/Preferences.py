import pickle


class Preferences:

    # TODO: add project folder to path
    file_path = "preferences.pkl"
    video_path = None
    data_path = None

    def __init__(self):
        self.load()

    def load(self):
        """Loads the saved values back into this class from a file"""
        f = open(self.file_path, 'rb')
        tmp_dict = pickle.load(f)
        f.close()

        self.__dict__.update(tmp_dict)

    def save(self):
        """Saves the values inside this class to a file"""
        f = open(self.file_path, 'wb')
        pickle.dump(self.__dict__, f)
        f.close()


if __name__ == '__main__':
    p = Preferences()
    # p.video_path = "test/videos"
    # p.save()
    print(p.video_path)
