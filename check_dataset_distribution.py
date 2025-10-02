import os

dataset_dir = 'dataset'  # If your dataset is in a different folder, change this path

print("\n📊 Class-wise image count:\n")

for cls in sorted(os.listdir(dataset_dir)):
    cls_path = os.path.join(dataset_dir, cls)
    if os.path.isdir(cls_path):
        count = len([f for f in os.listdir(cls_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp'))])
        print(f"🩸 {cls}: {count} images")
