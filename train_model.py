import os
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Rescaling
from keras.utils import image_dataset_from_directory

# Paths
dataset_path = 'dataset'
model_save_path = 'model/fingerprint_cnn_model.keras'
class_names_path = 'model/classes.txt'

# Image dimensions
img_height = 128
img_width = 128
batch_size = 16
epochs = 10

# Load datasets
raw_train_ds = image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size
)

raw_val_ds = image_dataset_from_directory(
    dataset_path,
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(img_height, img_width),
    batch_size=batch_size
)

# Get class labels
class_names = raw_train_ds.class_names
print("Detected Classes:", class_names)

# Save class names
os.makedirs(os.path.dirname(class_names_path), exist_ok=True)
with open(class_names_path, 'w') as f:
    for name in class_names:
        f.write(f"{name}\n")

# Normalize
normalization_layer = Rescaling(1./255)
train_ds = raw_train_ds.map(lambda x, y: (normalization_layer(x), y))
val_ds = raw_val_ds.map(lambda x, y: (normalization_layer(x), y))

# Build model
model = Sequential([
    Conv2D(32, (3, 3), activation='relu', input_shape=(img_height, img_width, 3)),
    MaxPooling2D((2, 2)),

    Conv2D(64, (3, 3), activation='relu'),
    MaxPooling2D((2, 2)),

    Flatten(),
    Dense(128, activation='relu'),
    Dense(len(class_names), activation='softmax')
])

model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# Train model
model.fit(train_ds, validation_data=val_ds, epochs=epochs)

# Save model
model.save(model_save_path)
print("Model trained and saved to:", model_save_path)

