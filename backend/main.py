import tensorflow as tf
import numpy as np
import os
import uuid
from datetime import datetime
import pytz
import hashlib
import json

from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from PIL import Image
import io
import cv2

from db import users_collection, history_collection
from grad import generate_gradcam

IST = pytz.timezone("Asia/Kolkata")

# MODEL
IMG_SIZE = (300, 300)

with open("class_names.txt", "r") as f:
    class_names = [line.strip() for line in f.readlines()]

preprocess_input = tf.keras.applications.efficientnet.preprocess_input

# EfficientNetB3 Base Model
base_model = tf.keras.applications.EfficientNetB3(
    input_shape=IMG_SIZE + (3,),
    include_top=False,
    weights="imagenet"
)

# Full Model Architecture (Same as Training)
inputs = tf.keras.Input(shape=IMG_SIZE + (3,))
x = preprocess_input(inputs)
x = base_model(x, training=False)

x = tf.keras.layers.GlobalAveragePooling2D()(x)
x = tf.keras.layers.Dropout(0.4)(x)

outputs = tf.keras.layers.Dense(len(class_names), activation="softmax")(x)

model = tf.keras.Model(inputs, outputs)

# Loading Checkpoint Weights
ckpt = tf.train.Checkpoint(model=model)
ckpt.restore("efficientnet_ckpt").expect_partial()

print("Checkpoint model loaded successfully")

# EfficientNet backbone reference
effnet = model.get_layer("efficientnetb3")

print("\n--- EfficientNetB3 Conv Layers ---")
for layer in effnet.layers:
    if "conv" in layer.name:
        print(layer.name)
print("--- END ---\n")


# DISEASE INFO FILE
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
info_path = os.path.join(BASE_DIR, "disease_info.json")

with open(info_path, "r", encoding="utf-8") as f:
    disease_info = json.load(f)

normalized_info = {k.lower().strip(): v for k, v in disease_info.items()}

# STORAGE
UPLOAD_DIR = "uploads"
GRADCAM_DIR = "gradcams"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(GRADCAM_DIR, exist_ok=True)

# APP 
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/uploads", StaticFiles(directory=UPLOAD_DIR), name="uploads")
app.mount("/gradcams", StaticFiles(directory=GRADCAM_DIR), name="gradcams")

BASE_URL = "http://localhost:8000"

# PASSWORD
def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(password: str, hashed: str) -> bool:
    return hashlib.sha256(password.encode()).hexdigest() == hashed

# AUTH
@app.post("/signup")
def signup(username: str = Form(...), password: str = Form(...)):
    if users_collection.find_one({"username": username}):
        return {"error": "User already exists"}

    users_collection.insert_one({
        "username": username,
        "password": hash_password(password)
    })

    return {"message": "Signup successful"}


@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    user = users_collection.find_one({"username": username})

    if not user or not verify_password(password, user["password"]):
        return {"error": "Invalid credentials"}

    return {
        "user_id": str(user["_id"]),
        "username": user["username"]
    }

# PREDICT
@app.post("/predict")
async def predict(file: UploadFile = File(...), user_id: str = Form(...)):

    image_bytes = await file.read()
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")

    img = img.resize((300, 300))

    uid = uuid.uuid4().hex
    image_path = f"{UPLOAD_DIR}/{uid}.jpg"
    gradcam_path = f"{GRADCAM_DIR}/{uid}.png"

    img.save(image_path)

    # Prepare Input
    img_array = np.expand_dims(np.array(img), axis=0)
    img_array = preprocess_input(img_array)

    # Prediction
    preds = model.predict(img_array)[0]

    idx = int(np.argmax(preds))
    confidence = round(float(np.max(preds)) * 100, 2)
    predicted_class = class_names[idx]

    # GradCAM
    try:
        heatmap = generate_gradcam(
            effnet,
            img_array,
            "top_conv"
        )

        heatmap = cv2.resize(heatmap, (300, 300))
        heatmap = np.uint8(255 * heatmap)

        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)

        original = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        overlay = cv2.addWeighted(original, 0.6, heatmap, 0.4, 0)

        cv2.imwrite(gradcam_path, overlay)
        print("GradCAM saved:", gradcam_path)

    except Exception as e:
        print("GradCAM Error:", e)
        gradcam_path = None

    # Disease Info
    info = normalized_info.get(predicted_class.lower().strip(), {})

    # Save History
    history_collection.insert_one({
        "user_id": user_id,
        "disease": predicted_class,
        "confidence": confidence,
        "image_url": f"/uploads/{uid}.jpg",
        "gradcam_url": f"/gradcams/{uid}.png" if gradcam_path else None,
        "symptoms": info.get("symptoms"),
        "cause": info.get("cause"),
        "prevention": info.get("prevention"),
        "cure": info.get("cure"),
        "timestamp": datetime.now(IST)
    })

    return {
        "disease": predicted_class,
        "confidence": confidence,
        "image_url": f"{BASE_URL}/uploads/{uid}.jpg",
        "gradcam_url": f"{BASE_URL}/gradcams/{uid}.png" if gradcam_path else None,
        "symptoms": info.get("symptoms"),
        "cause": info.get("cause"),
        "prevention": info.get("prevention"),
        "cure": info.get("cure")
    }

# HISTORY
@app.get("/history/{user_id}")
def get_history(user_id: str):

    records = history_collection.find({"user_id": user_id}).sort("timestamp", -1)
    result = []

    for r in records:
        ts = r.get("timestamp")
        formatted_date = ts.strftime("%d %b %Y") if ts else "Unknown date"

        result.append({
            "disease": r.get("disease"),
            "confidence": r.get("confidence"),
            "image_url": f"{BASE_URL}{r.get('image_url')}" if r.get("image_url") else None,
            "gradcam_url": f"{BASE_URL}{r.get('gradcam_url')}" if r.get("gradcam_url") else None,
            "symptoms": r.get("symptoms"),
            "cause": r.get("cause"),
            "prevention": r.get("prevention"),
            "cure": r.get("cure"),
            "date": formatted_date
        })

    return result

# MONTHLY TRENDS
@app.get("/monthly-trends/{user_id}")
def monthly_trends(user_id: str):

    pipeline = [
        {"$match": {"user_id": user_id, "timestamp": {"$exists": True}}},
        {"$group": {
            "_id": {
                "year": {"$year": "$timestamp"},
                "month": {"$month": "$timestamp"}
            },
            "count": {"$sum": 1}
        }},
        {"$sort": {"_id.year": 1, "_id.month": 1}}
    ]

    data = list(history_collection.aggregate(pipeline))

    result = []
    for item in data:
        month = item["_id"]["month"]
        year = item["_id"]["year"]

        result.append({
            "month": f"{year}-{str(month).zfill(2)}",
            "count": item["count"]
        })

    return result
