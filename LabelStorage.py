class LabelStorage:

    def __init__(self, filename):
        self.labels = {}
        self.filename = filename

    def addLabel(self, timestamp, label):
        self.labels[timestamp] = label

    def storeLabels(self):
        file = open(self.filename + ".labels", "w")

        # sort dict
        for timestamp in sorted(self.labels):
            file.write(str(timestamp) + '-' + self.labels[timestamp] + '\n')

    def loadLabels(self):
        file = open(self.filename + ".labels", "r")

        for line in file:
            line = line.rstrip('\n')
            split = line.split('-')
            self.labels[split[0]] = split[1]


if __name__ == '__main__':
    # write labels to file
    w = LabelStorage("test")
    w.addLabel(1, "walking")
    w.addLabel(1, "running")
    w.addLabel(3, "running")
    w.addLabel(2, "walking")
    w.storeLabels()

    # load labels from file
    r = LabelStorage("test")
    r.loadLabels()
    print(r.labels)
