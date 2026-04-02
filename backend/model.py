import matplotlib.pyplot as plt

models = ["MobileNetV2", "EffNetB0", "EffNetB1", "EffNetB2", "EffNetB3"]
accuracies = [63, 70, 82, 87, 90]

plt.figure(figsize=(9, 5))

plt.bar(models, accuracies)

plt.title("Model vs Accuracy Comparison")
plt.xlabel("Model")
plt.ylabel("Accuracy (%)")

# Add labels on bars
for i, acc in enumerate(accuracies):
    plt.text(i, acc + 0.5, f"{acc}%", ha='center')

plt.ylim(50, 100)
plt.grid(axis='y')

plt.show()