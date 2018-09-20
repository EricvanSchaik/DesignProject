class Sensor:

    def __init__(self, name, sampling_rate, unit):
        self.name = name
        self.sampling_rate = sampling_rate
        self.unit = unit

    def set_name(self, new_name):
        self.name = new_name

    def set_sampling_rate(self, new_sampling_rate):
        self.sampling_rate = new_sampling_rate

    def set_unit(self, new_unit):
        self.unit = new_unit
