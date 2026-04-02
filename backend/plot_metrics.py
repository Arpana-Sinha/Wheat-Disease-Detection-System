import json
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

LOG_FILE = "accuracy_log.json"

with open(LOG_FILE, "r") as f:
 runs = json.load(f)

# --------- Latest Run Learning Curves ---------

latest_run = runs[-1]

train_acc = latest_run["train_accuracy_curve"]
val_acc = latest_run["val_accuracy_curve"]
train_loss = latest_run["train_loss_curve"]
val_loss = latest_run["val_loss_curve"]

epochs_range = list(range(1, len(train_acc) + 1))

plt.figure(figsize=(12,5))

# Accuracy Curve

plt.subplot(1,2,1)
plt.plot(epochs_range, train_acc, label="Train Accuracy", linewidth=2)
plt.plot(epochs_range, val_acc, label="Validation Accuracy", linewidth=2)

# Mark start of fine-tuning (Stage 2)

plt.axvline(x=10, linestyle="--", color="gray", label="Fine-tuning Start")

plt.xlabel("Epochs")
plt.ylabel("Accuracy")
plt.title("Training vs Validation Accuracy (Learning Curve)")
plt.legend()
plt.grid(True)

# FIXED Y-AXIS: 70 80 90 100

ax = plt.gca()
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
plt.ylim(0.70, 1.00)
plt.yticks([0.70, 0.80, 0.90, 1.00])

# Loss Curve

plt.subplot(1,2,2)
plt.plot(epochs_range, train_loss, label="Train Loss", linewidth=2)
plt.plot(epochs_range, val_loss, label="Validation Loss", linewidth=2)

# Mark start of fine-tuning (Stage 2)

plt.axvline(x=10, linestyle="--", color="gray", label="Fine-tuning Start")

plt.xlabel("Epochs")
plt.ylabel("Loss")
plt.title("Training vs Validation Loss")
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# --------- Total Epochs vs Accuracy (Averaged) ---------

from collections import defaultdict
import numpy as np

epoch_groups = defaultdict(list)

# collect accuracies for each epoch

for run in runs:
 epoch = run["total_epochs"]
 acc = run["best_val_accuracy"]
 epoch_groups[epoch].append(acc)

# compute average accuracy for each epoch

epochs = []
avg_accuracies = []

for epoch in sorted(epoch_groups.keys()):
 epochs.append(epoch)
 avg_accuracies.append(np.mean(epoch_groups[epoch]))

plt.figure(figsize=(8,5))
plt.plot(epochs, avg_accuracies, marker="o", linewidth=2)

plt.xlabel("Total Epochs")
plt.ylabel("Average Validation Accuracy")
plt.title("Effect of Training Epochs on Accuracy")
plt.grid(True)

# FIXED Y-AXIS: 70 80 90 100

ax = plt.gca()
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1))
plt.ylim(0.70, 1.00)
plt.yticks([0.70, 0.80, 0.90, 1.00])

plt.show()
