import pickle


class Preferences:

    file_path = "preferences.pkl"
    video_path = ""
    data_path = ""

    def load(self):
        f = open(self.file_path, 'rb')
        tmp_dict = pickle.load(f)
        f.close()

        self.__dict__.update(tmp_dict)

    def save(self):
        f = open(self.file_path, 'wb')
        pickle.dump(self.__dict__, f)
        f.close()


if __name__ == '__main__':
    p = Preferences()
    # p.video_path = "data/videos"
    # p.save()
    p.load()
    print(p.video_path)
