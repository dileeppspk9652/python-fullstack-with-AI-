import numpy as np
import cv2
from tensorflow.keras.models import load_model, Model
from tensorflow.keras.utils import to_categorical

# === Load Models ===
cnn_model = load_model('model/fingerprint_cnn_model.keras')
gnn_model = load_model('model/fingerprint_gnn_model.keras')

# === Load Class Labels ===
labels_path = 'model/classes.txt'
with open(labels_path, 'r') as f:
    labels = [line.strip() for line in f.readlines()]

# === Load and Preprocess Image ===
img_path = 'static/scanned_fingerprint.bmp'
img = cv2.imread(img_path)
img = cv2.resize(img, (128, 128))
img = img / 255.0
img = np.expand_dims(img, axis=0)

# === Extract features from CNN ===
feature_extractor = Model(inputs=cnn_model.input, outputs=cnn_model.get_layer('feature_layer').output)
features = feature_extractor.predict(img)

# === Predict with GNN ===
prediction = gnn_model.predict(features)[0]
class_index = np.argmax(prediction)
label = labels[class_index]
confidence = round(prediction[class_index] * 100, 2)

print(f"✅ Predicted Blood Group: {label} ({confidence}%)")
