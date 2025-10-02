from tensorflow.keras.models import load_model

# Load the model
model = load_model('models/fingerprint_gnn_model.keras')

print("✅ Model loaded successfully.")
