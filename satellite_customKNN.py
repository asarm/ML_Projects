# -*- coding: utf-8 -*-
"""satellite.ipynb

Building a custom KNN model

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1frNckKrkjtJSPwyx8k9eVnsSzDBznlmU
"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import GridSearchCV
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error 
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math

# loading train and test data from URL
train_data = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/satimage/sat.trn', sep=' ', header=None)
test_data = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/statlog/satimage/sat.tst', sep=' ', header=None)
data = pd.DataFrame(np.concatenate((train_data, test_data)))

# Separating target value
col_indexes = [index for index in range(36)]
X = data[col_indexes]
y = data[[36]]

# creating custom train-test data with 70:30 ratio
 X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# converting train and test sets from df to numpy array for custom knn implementation
X_trainArr, X_testArr, y_trainArr, y_testArr = pd.DataFrame.to_numpy(X_train), pd.DataFrame.to_numpy(X_test), pd.DataFrame.to_numpy(y_train), pd.DataFrame.to_numpy(y_test)
dataArr = pd.DataFrame.to_numpy(data)

# calculates euclidean distance between two given data row  
def euclidean_distance(row1, row2):
	distance = 0.0
	for i in range(len(row1)-1):
		distance += (row1[i] - row2[i])**2
	return math.sqrt(distance)

# finds nearest row according to euclidean distance. Returns nearest 'num_neighbors' row.
def get_neighbors(train, test_row, num_neighbors):
	distances = []
	for train_row in train:
		dist = euclidean_distance(test_row[:-1], train_row[:-1])
		distances.append((train_row, dist))
	distances.sort(key=lambda tup: tup[1])
	neighbors = []
	for i in range(num_neighbors):
		neighbors.append(distances[i][0])
	return neighbors

# makes prediction for given row using get_neighbors(). Returns predicted value
# data is the entiring dataset, test is the row that user wants to predict 
def get_prediction(data, test, num_neighbors):
  neighbors = get_neighbors(data, test, num_neighbors)
  predicts = np.array([], dtype=np.int32)  
  for neighbor in neighbors:
    prediction = neighbor[-1]
    predicts = np.append(predicts, prediction)
  return(np.bincount(predicts).argmax())

# Returns accuracy score for given neighbors numbers as a dict
def get_score(data, X, y, neighbors):
  print("Total data lenght: "+ str(len(X)))
  # keeps accuracy score for each given neighbors value
  scores = {}
  for n in neighbors:
    score_arr = []
    print("-----------"+str(n)+"-----------")
    for i in range(len(X)):
      prediction = get_prediction(data, X[i], n)
      if (prediction == y[i]):
        score_arr.append(1)
      else:
        score_arr.append(0)
      if i % 350 == 0 and i != 0:
        print(i, score_arr.count(1)/len(score_arr))
    scores[n] = score_arr.count(1)/len(score_arr) 
  return scores

# Getting scores for different k values (3, 4, 5, 6, 7)
scores = get_score(dataArr, X_trainArr, y_trainArr, [3, 4, 5, 6, 7])

# Training accuracy scores for each k value
print(scores)
'''
{3: 0.9538188277087034,
 4: 0.9429396092362344,
 5: 0.9438277087033747,
 6: 0.9351687388987566,
 7: 0.9345026642984015}
 '''

# Plotting traning accuracy scores for each k value
# Best k value is 3 (95.38% accuracy for training set)
lists = sorted(scores.items())

x, y = zip(*lists)

plt.plot(x, y)
plt.show()

# score is 94.74% for test set
scores = get_score(X_test, y_test, [3])

"""USING KNN FROM SKLEARN"""

# using my found best n_neighbors (3) on sklearn knn model
nnModel = KNeighborsClassifier(n_neighbors=3).fit(X_train, y_train)
# score is %90
knnModel.score(X_test,y_test)

# Using grid search
knnModel2 = KNeighborsClassifier()
params = {
    "n_neighbors":[3,4,5,6,7],
          }
modelCV = GridSearchCV(knnModel2, params, cv=5)
modelCV.fit(X_train, y_train)

# best value for n_neighbors: 3
modelCV.best_estimator_.get_params()