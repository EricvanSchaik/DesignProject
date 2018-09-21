import time
import numpy as np
from random import randint
from sklearn.model_selection import train_test_split

import pandas as pd
from pandas import Series
from sklearn.naive_bayes import GaussianNB

from data_import.import_data import parse_csv


def classify(data, used_features, ground_truth, tags):
    """
    Makes class predictions for datasets.

    :param data: The dataset to classify.
    :param used_features: The features that should be used by the classifier.
    :param ground_truth: Current classifications that have been provided by the user. If a row has not been classified
        yet, then the row contains None.
    :return: list of tuples: First element of tuple is predicted class, second element is a list of probabilities for
        each class.
    """

    if len(data) != len(ground_truth):
        raise ValueError("len(data) != len(ground_truth)")

    # Add ground_truth column to the dataset
    data['ground_truth'] = Series(ground_truth)

    # Clean the dataset of entries that have not been classified yet to use as training set
    train_set = data[pd.notnull(data['ground_truth'])]

    gnb = GaussianNB()

    gnb.fit(
        train_set[used_features],
        train_set['ground_truth']
    )

    preds = gnb.predict(data[used_features])
    probs = gnb.predict_proba(data[used_features])

    res = []

    for i in range(0, len(preds)):
        res.append([tags[i], preds[i], round(max(probs[i][0], probs[i][1]), 2)])

    return res


if __name__ == "__main__":
    # data = parse_csv("../data/DATA-001.CSV")
    # ground_truth = []
    #
    # for i in range(0, len(data)):
    #     ground_truth.append(None)
    #
    # for i in range(0, int(len(data) / 2)):
    #     ground_truth[i * 2] = randint(0, 1)
    #
    # start_time = time.time()
    # print(classify(data, ["Ax", "Ay", "Az", "Gx", "Gy", "Gz"], ground_truth))
    # print("--- %s seconds ---" % (time.time() - start_time))
    data = pd.read_csv("train.csv")

    # Convert categorical variable to numeric
    data["Sex_cleaned"] = np.where(data["Sex"] == "male", 0, 1)
    data["Embarked_cleaned"] = np.where(data["Embarked"] == "S", 0,
                                        np.where(data["Embarked"] == "C", 1,
                                                 np.where(data["Embarked"] == "Q", 2, 3)
                                                 )
                                        )

    # Cleaning dataset of NaN
    data = data[[
        "PassengerId",
        "Survived",
        "Pclass",
        "Sex_cleaned",
        "Age",
        "SibSp",
        "Parch",
        "Fare",
        "Embarked_cleaned"
    ]].dropna(axis=0, how='any')

    used_features = [
        "Pclass",
        "Sex_cleaned",
        "Age",
        "SibSp",
        "Parch",
        "Fare",
        "Embarked_cleaned"
    ]

    ground_truth = data["Survived"]
    tags = list(data["PassengerId"])

    classes = classify(data, used_features, ground_truth, tags)

    print(classes)
    print(len(classes))
