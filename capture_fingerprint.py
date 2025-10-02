from pyfingerprint.pyfingerprint import PyFingerprint
import time
import cv2
import os

def capture_fingerprint_and_save(output_path):
    try:
        print("🔌 Connecting to R307S fingerprint sensor on COM5...")
        sensor = PyFingerprint('COM5', 57600, 0xFFFFFFFF, 0x00000000)

        if not sensor.verifyPassword():
            return False, '❌ Sensor password is incorrect!'

        print("🟢 Sensor ready. Waiting for finger...")
        while not sensor.readImage():
            time.sleep(0.5)

        print('🖐️ Finger detected.')
        sensor.convertImage(0x01)

        # Save BMP
        bmp_path = 'static/scanned_fingerprint.bmp'
        sensor.downloadImage(bmp_path)

        if not os.path.exists(bmp_path):
            return False, '❌ Image file was not saved.'

        print(f'✅ Fingerprint image saved to: {bmp_path}')

        # Save JPG preview
        img = cv2.imread(bmp_path)
        if img is None:
            return False, '❌ Failed to load downloaded image.'

        resized = cv2.resize(img, (128, 128))
        cv2.imwrite(output_path, resized)

        return True, '✅ Fingerprint captured and saved.'

    except Exception as e:
        return False, f'❌ {str(e)}'

if __name__ == "__main__":
    success, msg = capture_fingerprint_and_save('static/input.jpg')
    print(msg)
    exit(0 if success else 1)
