import pandas as pd
import numpy as np
import csv
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.svm import SVC
from sklearn.svm import LinearSVC
from sklearn import tree
import matplotlib.pyplot as plt
from sklearn.neural_network import MLPClassifier
from sklearn.svm import SVC
from sklearn.datasets import make_classification
from statistics import mode

from packetsniff.progress import ProgressDisplay

# read CSV including header
df = pd.read_csv("data/trainingSet.csv", header=0)
pf = pd.read_csv("data/flows.csv", header=0)

X = df[df.columns[:-1]] # use all columns except last one (type)
y = df['type']

predict = pf[pf.columns]

predictions = []

resultsDT = []
resultsNN = []
resultsSVC = []

acc_scores = 0

debug = False
try:
    live
except NameError:
    live = False

progress = ProgressDisplay("Training models... ", " tests ran")

if (live):
    testsize = 0
    testruns = 1
else:
    testsize = 0.25
    testruns = 10
testrunsprint = 20

for i in range(0, testruns):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = testsize)

    #Decision Trees
    clfDT = tree.DecisionTreeClassifier()
    clfDT.fit(X_train, y_train)
    #here you are supposed to calculate the evaluation measures indicated in the project proposal (accuracy, F-score etc)
    if not (live):
        resultsDT.append(clfDT.score(X_test, y_test))
    dtPrediction = clfDT.predict(predict)
    if (debug):
        print("DT Prediction: ", dtPrediction)

    # Neural network (MultiPerceptron Classifier)
    clfNN = MLPClassifier(max_iter=1000)
    clfNN.fit(X_train, y_train)
    if not (live):
        resultsNN.append(clfNN.score(X_test, y_test))
    nnPrediction = clfDT.predict(predict)
    if (debug):
        print("NN Prediction: ", nnPrediction)

    #SVM's
    clfSVC = SVC(kernel='linear')     #SVC USE THIS
    #clfSVC = LinearSVC()  #Linear SVC #max_iter = 100000
    clfSVC.fit(X_train, y_train)
    svcPrediction = clfSVC.predict(predict)
    if(debug):
        print("SVC Prediction: ", svcPrediction, "\n")
    #here you are supposed to calculate the evaluation measures indicated in the project proposal (accuracy, F-score etc)
    if not (live):
        resultsSVC.append(clfSVC.score(X_test, y_test))  #accuracy score -- score has to be output in graph form

    if len(set([dtPrediction[0], nnPrediction[0], svcPrediction[0]])) != len([dtPrediction[0], nnPrediction[0], svcPrediction[0]]):
        predictions.append(mode([dtPrediction[0], nnPrediction[0], svcPrediction[0]]))

    progress.next()
    if(debug):
        progress.newline()

progress.newline()


if not (live):
    print('Decision Tree: ' + str(sum(resultsDT)/len(resultsDT)))
    if (testruns <= testrunsprint):
        print(resultsDT)
    print('Support Vector Machine: ' + str(sum(resultsSVC)/len(resultsSVC)))
    if (testruns <= testrunsprint):
        print(resultsSVC)
    print('Neural Network: ' + str(sum(resultsNN)/len(resultsNN)))
    if (testruns <= testrunsprint):
        print(resultsNN)

finalPrediction = mode(predictions)
if finalPrediction == 1:
    finalPredictionString = "Web Browsing"
elif finalPrediction == 2:
    finalPredictionString = "Video Streaming"
elif finalPrediction == 3:
    finalPredictionString = "Video Conferencing"
else:
    finalPredictionString = "File Download"
print("\nFinal Prediction: ", finalPredictionString)

# print graph if small testrun count
if not (live):
    if (testruns <= testrunsprint):

        ind = np.arange(1, testruns+1 ,1)
        width = 0.2

        p1 = plt.bar(ind-width, resultsDT, width)
        p3 = plt.bar(ind, resultsSVC, width) #, bottom = resultsSVC)
        p2 = plt.bar(ind+width, resultsNN, width) # , bottom = resultsNN)

        plt.title('Evaluation')
        plt.xlabel('Test Run')
        plt.ylabel('Accuracy')
        plt.xticks(np.arange(1, testruns+1, 1))
        plt.yticks(np.arange(0, 1.1, 0.1))
        plt.ylim(top=1.0)
        plt.legend(('Decision Tree', 'Support Vector Machine', 'Neural Network'), loc = 'lower right')
        plt.show() # save button is available
        #plt.savefig('Evaluation.png')
