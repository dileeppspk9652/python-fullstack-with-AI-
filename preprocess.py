# preprocess.py

import cv2
import numpy as np

# Match this with your model's input
IMAGE_SIZE = (224, 224)

def preprocess_fingerprint(image_path):
    """
    Reads an image, resizes, normalizes, and returns a model-ready numpy array.
    """
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"Image not found at path: {image_path}")

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB
    img = cv2.resize(img, IMAGE_SIZE)
    img = img.astype('float32') / 255.0         # Normalize
    img = np.expand_dims(img, axis=0)           # Add batch dimension

    return img
