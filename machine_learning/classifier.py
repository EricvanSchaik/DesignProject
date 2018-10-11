import time

import pandas as pd
from pandas import Series
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier

from data_import.import_data import parse_csv
from machine_learning.preprocessor import get_data
from sklearn.model_selection import train_test_split


class Classifier:

    def __init__(self, classifier, data):
        self.classifier = classifier
        self.data = data

    def classify(self, used_features, ground_truth):
        """
        Makes class predictions for datasets.

        :param data: The dataset to classify
        :param used_features: The features that should be used by the classifier
        :param ground_truth: Current classifications that have been provided by the user. If a row has not been
            classified yet, then the row contains None.
        :return: list of tuples: First element of tuple is predicted class, second element is a list of probabilities
            for each class.
        """

        if len(self.data) != len(ground_truth):
            raise ValueError("len(data) != len(ground_truth)")

        # # Add ground_truth column to the dataset
        # data['ground_truth'] = Series(ground_truth)

        # # Clean the data set of entries that have not been classified yet (remove NaN 'ground_truth' rows)
        # train_set = data[pd.notnull(data['ground_truth'])]

        # gnb = GaussianNB()

        train_set, test_set = train_test_split(self.data, test_size=0.3)

        self.classifier.fit(
            train_set[used_features],
            train_set['Label']
        )

        preds = self.classifier.predict(test_set[used_features])
        probs = self.classifier.predict_proba(test_set[used_features])

        true_labels = list(test_set['Label'])
        times = list(test_set['Timestamp'])
        res = []

        if len(preds) == len(true_labels):
            for i in range(0, len(preds)):
                res.append([times[i], true_labels[i], preds[i], round(max(probs[i][0], probs[i][1]), 2)])

        return res


if __name__ == '__main__':
    data = get_data()
    ground_truth = data['Label']
    classifier = Classifier(GaussianNB(), data)

    start_time = time.time()
    res = sorted(classifier.classify(['Ax', 'Ay', 'Az', 'Gx', 'Gy', 'Gz'], ground_truth), key=lambda row: row[0])
    for i in range(0, 1000):
        print(res[i])
    print("--- %s seconds ---" % (time.time() - start_time))
