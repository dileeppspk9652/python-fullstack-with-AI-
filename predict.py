import numpy as np
import cv2
from tensorflow.keras.models import load_model
from config import CNN_MODEL_PATH, IMAGE_SIZE, CLASSES

IMG_PATH = "static/scanned_fingerprint.jpg"

# Load model
cnn_model = load_model(CNN_MODEL_PATH)

def preprocess_image(path):
    img = cv2.imread(path)  # Read image in BGR
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB
    img = cv2.resize(img, IMAGE_SIZE)           # Resize to (128, 128)
    img = img.astype("float32") / 255.0         # Normalize
    img = np.expand_dims(img, axis=0)           # Add batch dimension
    return img

def predict_blood_group(image_path):
    image = preprocess_image(image_path)
    prediction = cnn_model.predict(image)[0]
    predicted_index = np.argmax(prediction)
    predicted_label = CLASSES[predicted_index]
    confidence = round(100 * np.max(prediction), 2)
    return predicted_label, confidence

if __name__ == "__main__":
    result = predict_blood_group(IMG_PATH)
    print("Predicted Blood Group:", result[0])
    print("Confidence:", result[1], "%")
