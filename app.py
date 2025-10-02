import os
import numpy as np
from flask import Flask, render_template, request
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from capture_fingerprint import capture_fingerprint_and_save

# ==== CONFIG ====
UPLOAD_FOLDER = 'static/uploads'
MODEL_PATH = 'model/fingerprint_cnn_model.keras'
CLASSES_PATH = 'model/classes.txt'
IMG_HEIGHT, IMG_WIDTH = 128, 128

# ==== INIT ====
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# ==== Load CNN Model ====
cnn_model = load_model(MODEL_PATH)

# ==== Load Class Labels ====
with open(CLASSES_PATH, 'r') as f:
    class_names = [line.strip() for line in f.readlines()]

# ==== ROUTES ====

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    input_mode = request.form.get('inputMode')
    
    # Determine input source
    if input_mode == 'scan':
        output_path = os.path.join(UPLOAD_FOLDER, 'live_scan.jpg')
        success, message = capture_fingerprint_and_save(output_path)
        if not success:
            return f"<h3>{message}</h3><a href='/'>Try Again</a>"
        image_path = output_path
    else:
        if 'file' not in request.files or request.files['file'].filename == '':
            return "<h3>No file uploaded.</h3><a href='/'>Try Again</a>"
        file = request.files['file']
        image_path = os.path.join(UPLOAD_FOLDER, file.filename)
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        file.save(image_path)

    # ==== Preprocess Image ====
    img = load_img(image_path, target_size=(IMG_HEIGHT, IMG_WIDTH))
    img_array = img_to_array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    # ==== Predict ====
    preds = cnn_model.predict(img_array)[0]
    pred_index = np.argmax(preds)
    predicted_class = class_names[pred_index]
    confidence = round(preds[pred_index] * 100, 2)

    return render_template('result.html',
                           image_path=image_path,
                           blood_group=predicted_class,
                           confidence=confidence)

# ==== MAIN ====
if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)
