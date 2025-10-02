import serial
import time
import numpy as np
from PIL import Image

# Configuration
PORT = "COM5"
BAUD_RATE = 57600
SAVE_PATH = "static/scanned_fingerprint.bmp"
RESIZE_TO = (128, 128)

# Initialize serial connection
ser = serial.Serial(PORT, BAUD_RATE, timeout=1)
time.sleep(2)

# R307 Packet Constants
HEADER = b'\xEF\x01\xFF\xFF\xFF\xFF'  # Standard packet header
COMMAND_DOWNLOAD_IMAGE = b'\x01\x00\x03\x0A\x00\x0E'  # Download image command
PACKET_DATA_HEADER = b'\xEF\x01\xFF\xFF\xFF\xFF\x02'

def read_fingerprint():
    print("🟡 Waiting for finger placement...")
    ser.write(b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x03\x01\x00\x05')  # GenImg
    response = ser.read(12)
    if len(response) >= 12 and response[9] == 0x00:
        print("✅ Fingerprint image captured.")
        return True
    print("❌ Failed to capture fingerprint.")
    return False

def download_image():
    print("⬇️ Downloading image...")
    ser.write(HEADER + COMMAND_DOWNLOAD_IMAGE)

    image_data = bytearray()
    while True:
        packet = ser.read(9)  # Header (6) + Type (1) + Length (2)
        if len(packet) < 9:
            break
        if not packet.startswith(PACKET_DATA_HEADER):
            break
        packet_length = int.from_bytes(packet[7:9], byteorder='big')
        data = ser.read(packet_length)
        if data[-2:] == b'\xF5\xF5':  # End of image transfer
            break
        image_data.extend(data[:-2])  # Exclude checksum

    if len(image_data) < 192 * 192:
        print("❌ Incomplete image received.")
        return None

    print("📷 Assembling fingerprint image...")
    img_array = np.frombuffer(image_data[:192*192], dtype=np.uint8).reshape((192, 192))

    # Resize to 128x128 for model
    from cv2 import resize, INTER_AREA
    resized = resize(img_array, RESIZE_TO, interpolation=INTER_AREA)

    Image.fromarray(resized).save(SAVE_PATH, format="BMP")
    print(f"✅ Saved fingerprint image: {SAVE_PATH}")
    return SAVE_PATH

def run_fingerprint_scan():
    if read_fingerprint():
        return download_image()
    return None

if __name__ == "__main__":
    run_fingerprint_scan()
