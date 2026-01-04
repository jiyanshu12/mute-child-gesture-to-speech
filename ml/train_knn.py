import numpy as np
from sklearn.neighbors import KNeighborsClassifier
import pickle
import os

os.makedirs("ml", exist_ok=True)

# Dummy landmark data (21 points × x,y = 42 features)
X = [
    [0.1] * 42,   # HELLO
    [0.2] * 42,   # YES
    [0.3] * 42,   # NO
    [0.4] * 42,   # HELP
    [0.5] * 42    # WATER
]

y = ["HELLO", "YES", "NO", "HELP", "WATER"]

model = KNeighborsClassifier(n_neighbors=3)
model.fit(X, y)

with open("ml/gesture_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("✅ ML model trained and saved at ml/gesture_model.pkl")

