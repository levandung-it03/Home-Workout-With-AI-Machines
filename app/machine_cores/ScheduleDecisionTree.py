from app.models.Enums import Gender, Aim

import pandas as pd

from sklearn.tree import DecisionTreeClassifier # Import Decision Tree Classifier
from sklearn.model_selection import train_test_split # Import train_test_split function
from sklearn import metrics #Import scikit-learn metrics module for accuracy calculation

def scheduleDecide(age: int, gender: int, aim: int, weight: int, bodyFat: float):

    return None

# def core_scheduleDecision():
#     return None

scheduleDecide(30, Gender.GENDER_MALE, Aim.WEIGHT_UP, 60, 21.4)