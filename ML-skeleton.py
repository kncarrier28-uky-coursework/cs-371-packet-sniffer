import pandas as pd
import numpy as np
import csv
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn import tree


# read CSV including header
df = pd.read_csv("trainingSet.csv", header=0)
# You might not need this next line if you do not care about losing information about flow_id etc. All you actually need to
# feed your machine learning model are features and output label.
# columns_list = ['proto', 'feature_1', 'feature_2', 'feature_3', 'feature_4', 'label']
# df.columns = columns_list -- read headers from file
# features = ['proto', 'feature_1', 'feature_2', 'feature_3', 'feature_4']

X = df[df.columns[:-1]] # use all columns except last one (type)
y = df['type']

acc_scores = 0
for i in range(0, 10):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)

    #Decision Trees
    clf = tree.DecisionTreeClassifier()
    clf.fit(X_train, y_train)

    # Neural network (MultiPerceptron Classifier)
    # clf = MLPClassifier()
    # clf.fit(X_train, y_train)

    #SVM's
    # clf = SVC(gamma='auto')     #SVC USE THIS
    # clf = LinearSVC()  #Linear SVC
    # clf.fit(X_train, y_train)


    #here you are supposed to calculate the evaluation measures indicated in the project proposal (accuracy, F-score etc)
    result = clf.score(X_test, y_test)  #accuracy score
    print(result)
