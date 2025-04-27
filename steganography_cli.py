import argparse
import base64
import hashlib
from PIL import Image
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes  # add this import

def derive_key(password: str, salt: bytes = b'stego_salt') -> bytes:
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100_000,
        backend=default_backend()
    )
    return base64.urlsafe_b64encode(kdf.derive(password.encode()))



def hide(image_file_path, file_to_hide_path, output_file_path, password):
    try:
        with open(file_to_hide_path, "rb") as f:
            content = f.read()
    except Exception as e:
        print(f"Error occurred while reading the file: {e}")
        return

    key = derive_key(password)
    fernet = Fernet(key)
    encrypted_content = fernet.encrypt(content)

    binary_data = []
    for byte in encrypted_content:
        b = bin(byte)[2:].zfill(8)
        binary_data.extend(int(bit) for bit in b)

    # Add NULL terminator (32 zero bits)
    binary_data.extend([0] * 32)
    while len(binary_data) % 3:
        binary_data.append(0)

    im = Image.open(image_file_path)
    px = im.load()
    pos = 0

    for i in range(im.size[0]):
        for j in range(im.size[1]):
            if pos >= len(binary_data):
                break
            R, G, B = px[i, j][:3]
            bits = binary_data[pos:pos+3]
            bits += [0] * (3 - len(bits))
            px[i, j] = (
                (R & ~1) | bits[0],
                (G & ~1) | bits[1],
                (B & ~1) | bits[2],
            )
            pos += 3
        if pos >= len(binary_data):
            break

    im.save(output_file_path)
    print(f"File hidden successfully in '{output_file_path}'.")


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
        print("Decryption failed: Wrong password or corrupted data.")
        return

    try:
        with open(output_file_path, "wb") as f:
            f.write(decrypted)
        print(f"Extracted file saved to '{output_file_path}'.")
    except Exception as e:
        print(f"Error writing output file: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Steganography CLI tool to hide and extract any file in/from PNG images using AES encryption."
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # hide command
    hide_parser = subparsers.add_parser('hide', help='Hide any file into an image')
    hide_parser.add_argument('-i', '--image', required=True, help='Input image path (PNG)')
    hide_parser.add_argument('-t', '--text', required=True, help='File path to hide (any binary file)')
    hide_parser.add_argument('-o', '--output', required=True, help='Output image path')
    hide_parser.add_argument('--password', required=True, help='Password for encryption')

    # unhide command
    unhide_parser = subparsers.add_parser('unhide', help='Extract hidden file from image')
    unhide_parser.add_argument('-i', '--image', required=True, help='Image with hidden file')
    unhide_parser.add_argument('-t', '--text', required=True, help='Path to save extracted file')
    unhide_parser.add_argument('--password', required=True, help='Password for decryption')

    args = parser.parse_args()

    if args.command == 'hide':
        hide(args.image, args.text, args.output, args.password)
    elif args.command == 'unhide':
        unhide(args.image, args.text, args.password)


if __name__ == "__main__":
    main()
