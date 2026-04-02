import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

import tensorflow as tf
import json
import numpy as np
from sklearn.metrics import f1_score
from sklearn.utils.class_weight import compute_class_weight


gpus = tf.config.experimental.list_physical_devices('GPU')
if gpus:
    try:
        for gpu in gpus:
            tf.config.experimental.set_memory_growth(gpu, True)
        print("GPU Enabled:", gpus)
    except RuntimeError as e:
        print(e)


IMG_SIZE = (360, 360)

BATCH_SIZE = 8

STAGE1_EPOCHS = 15
STAGE2_EPOCHS = 45

TRAIN_PATH = r"C:\Users\sarpa\.cache\kagglehub\datasets\kushagra3204\wheat-plant-diseases\versions\6\data\train"
VAL_PATH   = r"C:\Users\sarpa\.cache\kagglehub\datasets\kushagra3204\wheat-plant-diseases\versions\6\data\valid"

LOG_FILE = os.path.join(os.path.dirname(__file__), "accuracy_log.json")


train_ds_full = tf.keras.utils.image_dataset_from_directory(
    TRAIN_PATH,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE,
    shuffle=True,
    seed=42
)

val_ds = tf.keras.utils.image_dataset_from_directory(
    VAL_PATH,
    image_size=IMG_SIZE,
    batch_size=BATCH_SIZE
)

train_size = int(0.7 * len(train_ds_full))
train_ds = train_ds_full.take(train_size)

class_names = train_ds.class_names
num_classes = len(class_names)

train_ds = train_ds.apply(tf.data.experimental.ignore_errors())
val_ds   = val_ds.apply(tf.data.experimental.ignore_errors())


labels = np.concatenate([y.numpy() for _, y in train_ds])

class_weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(labels),
    y=labels
)

class_weights = dict(enumerate(class_weights))
class_weights = {k: float(v) for k, v in class_weights.items()}

print("Class Weights:", class_weights)


data_augmentation = tf.keras.Sequential([
    tf.keras.layers.RandomFlip("horizontal"),
    tf.keras.layers.RandomRotation(0.1),
    tf.keras.layers.RandomZoom(0.15),
])


preprocess_input = tf.keras.applications.efficientnet.preprocess_input

AUTOTUNE = tf.data.AUTOTUNE

train_ds = train_ds.map(
    lambda x, y: (data_augmentation(x, training=True), y),
    num_parallel_calls=AUTOTUNE
)

val_ds = val_ds.map(
    lambda x, y: (x, y),
    num_parallel_calls=AUTOTUNE
)

train_ds = train_ds.prefetch(AUTOTUNE)
val_ds   = val_ds.prefetch(AUTOTUNE)


base_model = tf.keras.applications.EfficientNetB3(
    input_shape=IMG_SIZE + (3,),
    include_top=False,
    weights="imagenet"
)

base_model.trainable = False

inputs = tf.keras.Input(shape=IMG_SIZE + (3,))

x = preprocess_input(inputs)

x = base_model(x, training=False)

x = tf.keras.layers.GlobalAveragePooling2D()(x)
x = tf.keras.layers.Dropout(0.4)(x)

outputs = tf.keras.layers.Dense(
    num_classes,
    activation="softmax"
)(x)

model = tf.keras.Model(inputs, outputs)


model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=1.5e-4),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)


early_stop = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True
)

reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.3,
    patience=3,
    verbose=1
)


print("\n--- STAGE 1 TRAINING ---\n")

history1 = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=STAGE1_EPOCHS,
    callbacks=[early_stop, reduce_lr],
    class_weight=class_weights
)


print("\n--- STAGE 2 TRAINING ---\n")

base_model.trainable = True

for layer in base_model.layers[:-100]:
    layer.trainable = False

model.compile(
    optimizer=tf.keras.optimizers.Adam(learning_rate=3e-5),
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

history2 = model.fit(
    train_ds,
    validation_data=val_ds,
    epochs=STAGE2_EPOCHS,
    callbacks=[early_stop, reduce_lr],
    class_weight=class_weights
)


train_acc = history1.history["accuracy"] + history2.history["accuracy"]
val_acc   = history1.history["val_accuracy"] + history2.history["val_accuracy"]

train_loss = history1.history["loss"] + history2.history["loss"]
val_loss   = history1.history["val_loss"] + history2.history["val_loss"]

best_val_accuracy = max(val_acc)


y_true, y_pred = [], []

for images, labels in val_ds:
    preds = model.predict(images, verbose=0)
    preds = np.argmax(preds, axis=1)
    y_true.extend(labels.numpy())
    y_pred.extend(preds)

final_f1 = f1_score(y_true, y_pred, average="macro")

print("\n==============================")
print(" Best Validation Accuracy:", best_val_accuracy)
print(" Final F1 Score:", final_f1)
print("==============================\n")


run_data = {
    "total_epochs": int(len(train_acc)),
    "best_val_accuracy": float(best_val_accuracy),
    "final_f1": float(final_f1),
    "train_accuracy_curve": [float(x) for x in train_acc],
    "val_accuracy_curve": [float(x) for x in val_acc],
    "train_loss_curve": [float(x) for x in train_loss],
    "val_loss_curve": [float(x) for x in val_loss],
    "class_weights": {str(k): float(v) for k, v in class_weights.items()}
}

if os.path.exists(LOG_FILE):
    with open(LOG_FILE, "r") as f:
        all_runs = json.load(f)
else:
    all_runs = []

all_runs.append(run_data)

with open(LOG_FILE, "w") as f:
    json.dump(all_runs, f, indent=4)

print("Saved to accuracy_log.json")


ckpt = tf.train.Checkpoint(model=model)
ckpt.write("efficientnet_ckpt")
print("Checkpoint saved successfully")