import json
import matplotlib.pyplot as plt
import os

FILE = os.path.join(os.path.dirname(__file__), "learning_curve.json")

with open(FILE, "r") as f:
    data = json.load(f)

latest = data[-1]

fractions = latest["fractions"]
accuracies = latest["val_accuracies"]

fractions_percent = [f * 100 for f in fractions]

plt.figure()

plt.plot(fractions_percent, accuracies, marker='o')

plt.xlabel("Training Data Size (%)")
plt.ylabel("Validation Accuracy")
plt.title("Learning Curve")

plt.ylim(0.7, 1.0)
plt.yticks([0.7, 0.8, 0.9, 1.0])

plt.grid()

plt.show()