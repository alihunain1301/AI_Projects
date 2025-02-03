# -*- coding: utf-8 -*-
"""Naive Bayes.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1MYsd3HpXnTsBUF7XYKTcVcsdPmR2_oHB
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

file_path = "heart.csv"  # Ensure this file is uploaded in the Colab environment
data = pd.read_csv("/content/heart.csv")

# Step 3: Display basic information about the dataset
print("Dataset Overview:")
print(data.head())
#print(data)

# Step 4: Features (X) and target (y)
X = data.drop(columns=["target"])  # Independent variables
y = data["target"]  # Dependent variable

# Step 5: Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 6: Initialize the Gaussian Naive Bayes model
model = GaussianNB()
# Step 7: Train the model
model.fit(X_train, y_train)

X_train

y_train

X_test

y_test

# Step 8: Make predictions
y_pred = model.predict(X_test)

# Step 9: Evaluate the model
print("Model Performance:")
print(f"Accuracy: {accuracy_score(y_test, y_pred):.2f}")

print("Confusion Matrix:")
print(confusion_matrix(y_test, y_pred))

print("Classification Report:")
print(classification_report(y_test, y_pred))