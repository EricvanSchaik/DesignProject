import numpy as np

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB

from datastorage import labelstorage as ls
from data_import import label_data as ld
from data_import import sensor_data as sd
from data_import import sensor_data_test as sdt
from data_export import windowing as wd


class Classifier:

    def __init__(self, classifier, sensor_data: sd.SensorData, label_data: ld.LabelData, label_col: str='Label',
                 timestamp_col: str='Timestamp'):
        self.classifier = classifier
        self.sensor_data = sensor_data.data
        self.label_data = label_data.get_data()
        self.label_col = label_col
        self.timestamp_col = timestamp_col

        self.add_labels_to_data()
        self.sensor_data = wd.windowing(self.sensor_data, self.label_col, self.timestamp_col)

    def get_sensor_data(self):
        return self.sensor_data

    def add_labels_to_data(self):
        """
        Add a label column to a DataFrame and fill it with provided labels.

        :param label_col: The name of the label column.
        :param timestamp_col: The name of the timestamp column.
        :return: Sensor data DataFrame where a label column has been added.
        """
        START_TIME_INDEX = 0
        STOP_TIME_INDEX = 1
        LABEL_INDEX = 2

        # Add Label column to the DataFrame and initialize it to NaN
        self.sensor_data[self.label_col] = np.nan

        for label_entry in self.label_data:
            start_time = label_entry[START_TIME_INDEX]
            stop_time = label_entry[STOP_TIME_INDEX]
            label = label_entry[LABEL_INDEX]

            # Add label to the corresponding rows in the sensor data
            self.sensor_data.loc[
                (self.sensor_data[self.timestamp_col] >= start_time) & (self.sensor_data[self.timestamp_col] < stop_time),
                self.label_col
            ] = label

        # Drop rows where the label is NaN (no label data available)
        self.sensor_data = self.sensor_data.dropna(subset=[self.label_col])

    def classify(self, used_features: [str]):
        """
        Makes class predictions for datasets.

        :param data: The dataset to classify
        :param used_features: The features that should be used by the classifier
        :param ground_truth: Current classifications that have been provided by the user. If a row has not been
            classified yet, then the row contains None.
        :return: list of tuples: First element of tuple is predicted class, second element is a list of probabilities
            for each class.
        """
        train_set, test_set = train_test_split(self.sensor_data, test_size=0.3)

        self.classifier.fit(
            train_set[used_features],
            train_set['Label']
        )

        preds = self.classifier.predict(test_set[used_features])
        probs = self.classifier.predict_proba(test_set[used_features])

        true_labels = list(test_set['Label'])
        res = []

        if len(preds) == len(true_labels):
            for i in range(0, len(preds)):
                res.append([preds[i], round(max(probs[i][0], probs[i][1]), 2)])

        return res


if __name__ == '__main__':
    SENSOR_FILE = 'data/20180515_09-58_CCDC301661B33D7_sensor.csv'
    PROJECT_DIR = 'test_project'
    SENSOR_ID = 'CCDC301661B33D7'

    sensor_data = sd.SensorData(SENSOR_FILE, sdt.test_settings())
    label_manager = ls.LabelManager(PROJECT_DIR)
    label_data = ld.LabelData(SENSOR_ID, label_manager)

    sensor_data.add_timestamp_column('Time', 'Timestamp')
    sensor_data.add_column_from_func("Vector", "sqrt(Ax^2 + Ay^2 + Az^2)")
    clsf = Classifier(GaussianNB(), sensor_data, label_data)
    print(clsf.get_sensor_data()[['Time', 'Vector']])
    # res = clsf.classify(['Vector'])
    #
    # for x in res:
    #     print(x)
