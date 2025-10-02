import time
import struct

def create_bmp_header(width=256, height=288):
    header_size = 62
    filesize = header_size + width * height

    header = bytearray([
        0x42, 0x4D,                    # Signature 'BM'
        filesize & 0xFF, (filesize >> 8) & 0xFF, (filesize >> 16) & 0xFF, (filesize >> 24) & 0xFF,
        0x00, 0x00, 0x00, 0x00,        # Reserved
        0x3E, 0x00, 0x00, 0x00,        # Offset to image data (62 bytes)
        0x28, 0x00, 0x00, 0x00,        # Info header size
        width & 0xFF, (width >> 8) & 0xFF, 0x00, 0x00,
        height & 0xFF, (height >> 8) & 0xFF, 0x00, 0x00,
        0x01, 0x00,                    # Planes
        0x08, 0x00,                    # Bits per pixel (8-bit grayscale)
        0x00, 0x00, 0x00, 0x00,        # Compression (none)
        0x00, 0x00, 0x00, 0x00,        # Image size
        0x00, 0x00, 0x00, 0x00,        # X pixels per meter
        0x00, 0x00, 0x00, 0x00,        # Y pixels per meter
        0x00, 0x00, 0x00, 0x00,        # Total colors
        0x00, 0x00, 0x00, 0x00         # Important colors
    ])

    # Grayscale palette
    for i in range(256):
        header.extend([i, i, i, 0])

    return header


def download_fingerprint_image(ser):
    time.sleep(1.5)  # Let the buffer settle

    # ✅ Step: Send Upload Image command directly (skip Img2Buf)
    upload_cmd = b'\xEF\x01\xFF\xFF\xFF\xFF\x01\x00\x03\x0A\x00\x0E'
    print("📤 Sending UpImage command...")
    ser.write(upload_cmd)

    image_data = bytearray()
    packet_count = 0

    while True:
        header = ser.read(9)
        if len(header) < 9:
            print("❌ Incomplete packet header.")
            break

        pid = header[6:7]
        if pid not in [b'\x02', b'\x08']:  # Data or End packet
            print(f"❌ Invalid packet header: {header}")
            break

        length = struct.unpack(">H", header[7:9])[0] - 2
        data = ser.read(length + 2)
        if len(data) < length + 2:
            print("❌ Incomplete image packet.")
            break

        image_data.extend(data[:-2])
        packet_count += 1

        if pid == b'\x08':
            break

    print(f"📦 Received {len(image_data)} bytes in {packet_count} packets.")

    if len(image_data) > 10000:
        bmp = create_bmp_header() + image_data
        return bmp
    else:
        print("❌ Image data is incomplete or corrupt.")
        return None
