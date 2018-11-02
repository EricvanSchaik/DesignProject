import datetime
import numpy as np
import pandas as pd

from sklearn.naive_bayes import GaussianNB

from datastorage import labelstorage as ls
from data_import import label_data as ld
from data_import import sensor_data as sd
from data_import import sensor_data_test as sdt
from data_export import windowing as wd


CLASSIFIER_NAN = 'NaN'

PRED_TIME_INDEX = 0
PRED_LABEL_INDEX = 1
PRED_PROBABILITY_INDEX = 2

PRED_PROB_THRESHOLD = 0.9
PRED_AMOUNT_THRESHOLD = 2


def make_predictions(preds: []):
    temp = []
    res = []

    for i in range(0, len(preds) - 1):
        pred = preds[i]
        next = preds[i + 1]

        temp.append(pred)

        if pred[PRED_LABEL_INDEX] != next[PRED_LABEL_INDEX]:
            avg_prob = sum(x[PRED_PROBABILITY_INDEX] for x in temp) / len(temp)

            if avg_prob >= PRED_PROB_THRESHOLD and len(temp) >= PRED_AMOUNT_THRESHOLD:
                res.append({
                    'begin': temp[0][PRED_TIME_INDEX],
                    'end': temp[len(temp) - 1][PRED_TIME_INDEX],
                    'label': temp[0][PRED_LABEL_INDEX],
                    'avg_probability': avg_prob
                })

            temp = []

    return res


class Classifier:
    def __init__(self, classifier=None, df: pd.DataFrame=None, features: [str]=None, label_col: str= 'Label',
                 timestamp_col: str='Timestamp'):
        self.classifier = classifier
        self.df = df
        self.features = features
        self.label_col = label_col
        self.timestamp_col = timestamp_col

    def set_classifier(self, classifier):
        self.classifier = classifier

    def set_df(self, df):
        self.df = df

    def set_features(self, features):
        self.features = features

    def classify(self):
        """
        Makes class predictions for datasets.
        """
        if self.classifier is None:
            raise ValueError('self.classifier is None')
        if self.df is None:
            raise ValueError('self.df is None')
        if self.features is None:
            raise ValueError('self.features is None')

        train_set = self.df[self.df[self.label_col] != CLASSIFIER_NAN]
        test_set = self.df[self.df[self.label_col] == CLASSIFIER_NAN]

        test_set_timestamps = list(test_set.index.strftime('%Y-%m-%d %H:%M:%S.%f'))

        self.classifier.fit(
            train_set[self.features],
            train_set[self.label_col]
        )

        preds = self.classifier.predict(test_set[self.features])
        probs = self.classifier.predict_proba(test_set[self.features])

        res = []

        for i in range(0, len(preds)):
            probability = max(probs[i])
            res.append([test_set_timestamps[i], preds[i], probability])

        return res


if __name__ == '__main__':
    SENSOR_FILE = 'data/20180515_09-58_CCDC301661B33D7_sensor.csv'
    PROJECT_DIR = 'test_project'
    SENSOR_ID = 'CCDC301661B33D7'

    LABEL_COL = 'Label'
    TIME_COL = 'Time'
    TIMESTAMP_COL = 'Timestamp'

    sensor_data = sd.SensorData(SENSOR_FILE, sdt.test_settings())
    label_manager = ls.LabelManager(PROJECT_DIR)
    label_data = ld.LabelData(label_manager, SENSOR_ID)

    # Prepare the sensor data for use by classifier
    sensor_data.add_timestamp_column(TIME_COL, TIMESTAMP_COL)
    sensor_data.add_column_from_func('accel', 'sqrt(Ax^2 + Ay^2 + Az^2)')
    sensor_data.add_column_from_func('gyro', 'sqrt(Gx^2 + Gy^2 + Gz^2)')
    sensor_data.add_labels(label_data.get_data(), LABEL_COL, TIMESTAMP_COL)
    data = sensor_data.get_data()

    # Remove data points where label == 'unknown'
    data = data[data.Label != 'unknown']

    window_cols = ['accel', 'gyro']
    used_cols = []
    funcs = {
        'mean': np.mean,
        'median': np.median,
        'std': np.std,
    }

    for func in funcs:
        for col in window_cols:
            used_cols.append('%s_%s' % (col, func))

    df = wd.windowing(data, window_cols, LABEL_COL, TIMESTAMP_COL, **funcs)
    clsf = Classifier(GaussianNB(), df, used_cols)
    res = clsf.classify()

    print(make_predictions(res))
