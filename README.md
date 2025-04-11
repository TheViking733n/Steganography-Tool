# Advanced Steganography CLI Tool 🔐🖼️

This is a **group project for Cybersecurity CS558**.

## 👥 Team Members

- Anant Prakash Singh  
- Anshul Mittal  
- Edgar Aditya Thorpe  
- Vavadiya Harsh  

---

## 📝 Project Description

This project develops an **advanced LSB steganography tool** featuring:

- 🔒 **AES Encryption** (planned)
- 🧠 **Adaptive Encoding**
- 🛡️ **Steganalysis Resistance**
- 🎯 **Minimal Visual Distortion**
- 🔁 **Seamless Extraction**
- 🧑‍💻 **User-Friendly Interface**

It ensures **high security** and **robustness** while embedding or extracting sensitive data within images.

---

## 📦 Current Status

> The project is currently in the **CLI phase**, implemented via a Python command-line tool.

Main code file: `steganography_cli.py`

---

## 🚀 Usage Guide

### 📥 Hide Text in Image

```bash
python steganography_cli.py hide -i input.png -t secret.txt -o output.png
```

- `-i`, `--image`: Path to input image (PNG format recommended)
- `-t`, `--text`: Path to `.txt` file containing the message to hide
- `-o`, `--output`: Output image path where text will be hidden

---

### 📤 Extract Text from Image

```bash
python steganography_cli.py unhide -i output.png -t extracted.txt
```

- `-i`, `--image`: Image with hidden text
- `-t`, `--text`: Path to save extracted text file

---

## 🛠️ Setup

Install dependencies:

```bash
pip install pillow
```

---

## 🏁 Roadmap

- ✅ CLI Tool with LSB Embedding/Extraction
- ⏳ Add AES Encryption for secure content
- ⏳ Build GUI-based cross-platform desktop app


---
