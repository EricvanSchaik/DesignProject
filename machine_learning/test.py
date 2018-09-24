import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import time
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier

# Importing dataset
data = pd.read_csv("train.csv")

print(len(data))

# Convert categorical variable to numeric
data["Sex_cleaned"] = np.where(data["Sex"] == "male", 0, 1)
data["Embarked_cleaned"] = np.where(data["Embarked"] == "S", 0,
                                    np.where(data["Embarked"] == "C", 1,
                                             np.where(data["Embarked"] == "Q", 2, 3)
                                             )
                                    )

# Cleaning dataset of NaN
data = data[[
    "Survived",
    "Pclass",
    "Sex_cleaned",
    "Age",
    "SibSp",
    "Parch",
    "Fare",
    "Embarked_cleaned"
]].dropna(axis=0, how='any')

# Split dataset in training and test datasets
X_train, X_test = train_test_split(data, test_size=0.5, random_state=int(time.time()))

# gnb = GaussianNB()
gnb = DecisionTreeClassifier()
used_features = [
    "Pclass",
    "Sex_cleaned",
    "Age",
    "SibSp",
    "Parch",
    "Fare",
    "Embarked_cleaned"
]

# Train classifier
gnb.fit(
    X_train[used_features],
    X_train["Survived"]
)

y_pred = gnb.predict(X_test[used_features])

# Print results
print("Number of mislabeled points out of a total {} points : {}, performance {:05.2f}%".format(
    X_test.shape[0],
    (X_test["Survived"] != y_pred).sum(),
    100 * (1 - (X_test["Survived"] != y_pred).sum() / X_test.shape[0])
))

y_prob = gnb.predict_proba(X_test[used_features])

res = []

for i in range(0, len(y_pred)):
    res.append((y_pred[i], y_prob[i][0]))

print(res)
