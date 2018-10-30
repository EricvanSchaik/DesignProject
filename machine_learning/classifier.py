import numpy as np
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import f1_score

from datastorage import labelstorage as ls
from data_import import label_data as ld
from data_import import sensor_data as sd
from data_import import sensor_data_test as sdt
from data_export import windowing as wd


class Classifier:

    def __init__(self, classifier, df: pd.DataFrame, used_cols: [str], label_col: str='Label', timestamp_col: str='Timestamp'):
        self.classifier = classifier
        self.df = df
        self.used_cols = used_cols
        self.label_col = label_col
        self.timestamp_col = timestamp_col

    def classify(self):
        """
        Makes class predictions for datasets.

        :param data: The dataset to classify
        :param used_features: The features that should be used by the classifier
        :param ground_truth: Current classifications that have been provided by the user. If a row has not been
            classified yet, then the row contains None.
        :return: list of tuples: First element of tuple is predicted class, second element is a list of probabilities
            for each class.
        """
        train_set, test_set = train_test_split(self.df, test_size=0.5, random_state=0)

        self.classifier.fit(
            train_set[self.used_cols],
            train_set[self.label_col]
        )

        preds = self.classifier.predict(test_set[self.used_cols])
        probs = self.classifier.predict_proba(test_set[self.used_cols])

        true_labels = list(test_set[self.label_col])
        res = []

        # for i in range(0, len(preds)):
        #     # if preds[i] != true_labels[i]:
        #         probability = round(max(probs[i]), 2)
        #         res.append([preds[i], true_labels[i], probability])

        return true_labels, preds


if __name__ == '__main__':
    SENSOR_FILE = 'data/20180515_09-58_CCDC301661B33D7_sensor.csv'
    PROJECT_DIR = 'test_project'
    SENSOR_ID = 'CCDC301661B33D7'

    LABEL_COL = 'Label'
    TIME_COL = 'Time'
    TIMESTAMP_COL = 'Timestamp'

    sensor_data = sd.SensorData(SENSOR_FILE, sdt.test_settings())
    label_manager = ls.LabelManager(PROJECT_DIR)
    label_data = ld.LabelData(SENSOR_ID, label_manager)

    # Prepare the sensor data for use by classifier
    sensor_data.add_timestamp_column(TIME_COL, TIMESTAMP_COL)
    sensor_data.add_column_from_func('accel', 'sqrt(Ax^2 + Ay^2 + Az^2)')
    sensor_data.add_column_from_func('gyro', 'sqrt(Gx^2 + Gy^2 + Gz^2)')
    sensor_data.add_labels(label_data.get_data(), LABEL_COL, TIMESTAMP_COL)
    data = sensor_data.get_data()

    # Remove data points where label == 'unknown'
    data = data[data.Label != 'unknown']

    window_cols = ['accel', 'gyro']
    used_cols = ['accel_mean', 'accel_std', 'gyro_mean', 'gyro_std']

    funcs = {
        'mean': np.mean,
        'std': np.std,
    }

    df = wd.windowing2(data, window_cols, LABEL_COL, TIMESTAMP_COL, **funcs)
    clsf = Classifier(GaussianNB(), df, used_cols)
    # res = clsf.classify()

    # for pred in res:
    #     print(pred)

    true, preds = clsf.classify()

    print(f1_score(true, preds, average='micro'))
