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

# read CSV including header
df = pd.read_csv("data/trainingSet.csv", header=0)

X = df[df.columns[:-1]] # use all columns except last one (type)
y = df['type']
resultsDT = []
resultsNN = []
resultsSVC = []

acc_scores = 0
for i in range(0, 10):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.25)

    #Decision Trees
    clfDT = tree.DecisionTreeClassifier()
    clfDT.fit(X_train, y_train)
    #here you are supposed to calculate the evaluation measures indicated in the project proposal (accuracy, F-score etc)
    resultsDT.append(clfDT.score(X_test, y_test))

    # Neural network (MultiPerceptron Classifier)
    clfNN = MLPClassifier(max_iter=1000)
    clfNN.fit(X_train, y_train)
    resultsNN.append(clfNN.score(X_test, y_test))

    #SVM's
    clfSVC = SVC(kernel='linear')     #SVC USE THIS
    #clfSVC = LinearSVC()  #Linear SVC #max_iter = 100000
    clfSVC.fit(X_train, y_train)
    resultsSVC.append(clfSVC.score(X_test, y_test))  #accuracy score -- score has to be output in graph form

print('Decision Tree: ' + str(resultsDT))
print('Support Vector Machine: ' + str(resultsSVC))
print('Neural Network: ' + str(resultsNN))

ind = np.arange(1,11,1)
width = 0.2

p1 = plt.bar(ind-width, resultsDT, width)
p3 = plt.bar(ind, resultsSVC, width) #, bottom = resultsSVC)
p2 = plt.bar(ind+width, resultsNN, width) # , bottom = resultsNN)

plt.title('Evaluation')
plt.xlabel('Test Run')
plt.ylabel('Accuracy')
plt.xticks(np.arange(1, 11, 1))
plt.yticks(np.arange(0, 1.1, 0.1))
plt.ylim(top=1.0)
plt.legend(('Decision Tree', 'Support Vector Machine', 'Neural Network'), loc = 'lower right')
plt.show() # save button is available
#plt.savefig('Evaluation.png')
