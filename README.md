# 🌾 Wheat Disease Detection System

A deep learning-based system for detecting wheat plant diseases using image classification. This project uses **EfficientNetB3** with transfer learning to achieve high accuracy in identifying multiple disease classes.

---

## 🚀 Features

* 🌱 Image-based wheat disease classification
* 🧠 EfficientNetB3 pretrained model (transfer learning)
* 📊 Training with accuracy + F1 score tracking
* ⚖️ Handles class imbalance using class weights
* 🔄 Two-stage training (feature extraction + fine-tuning)
* 📈 Training metrics logging and visualization
* 🖼️ Grad-CAM visualization support

---

## 🧠 Model Details

* **Architecture:** EfficientNetB3
* **Input Size:** 360 × 360
* **Training Strategy:**

  * Stage 1: Freeze base model
  * Stage 2: Fine-tune top layers
* **Loss Function:** Sparse Categorical Crossentropy
* **Optimizer:** Adam
* **Metrics:** Accuracy, F1 Score

---

## 📁 Project Structure

```
backend/
│
├── train_model.py        # Training pipeline
├── model.py              # Model definition
├── main.py               # Backend / API entry
├── db.py                 # Database connection
├── grad.py               # Grad-CAM logic
│
├── accuracy_log.json     # Training logs
├── learning_curve.json   # Metrics data
│
├── uploads/              # User uploaded images (ignored in Git)
├── gradcams/             # Grad-CAM outputs (ignored in Git)
│
└── .env                  # Environment variables (not tracked)
```


## 📊 Model Performance

* Achieved high validation accuracy using EfficientNetB3
* Improved performance with fine-tuning and class balancing
* F1 Score used for better evaluation on imbalanced data

---

## ⚠️ Notes

* Model weights are **not included** in the repository
* Large files (datasets, checkpoints) are excluded using `.gitignore`
* Upload your trained model separately if needed

---

## 📌 Future Improvements

* Deploy as a web/mobile application
* Add real-time disease detection
* Improve dataset size and diversity
* Integrate cloud model hosting

