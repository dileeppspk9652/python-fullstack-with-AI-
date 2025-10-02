import serial

PORT = "COM5"
BAUD_RATES = [57600, 9600, 115200]  # try all

for baud in BAUD_RATES:
    print(f"\n🔍 Testing baud rate: {baud}")
    try:
        ser = serial.Serial(PORT, baudrate=baud, timeout=2)
        print(f"🔌 Connected at {baud}")
        test_cmd = b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x03\x01\x00\x05'  # GenImg
        ser.write(test_cmd)
        resp = ser.read(12)
        print(f"📥 Response: {resp}")
        ser.close()
    except Exception as e:
        print(f"❌ Failed at baud {baud}: {e}")
