# 🛡️ Spam Detector

A desktop application built using PySide6 that detects spam messages using machine learning and provides an interactive UI experience.

This project was created to explore GUI development, audio integration, and basic ML pipeline implementation in Python.

---

## 🚀 Features

- 🧠 Spam detection using trained ML model
- 🎨 Clean UI built with PySide6
- 🔊 Sound effects integration
- 🔤 Custom fonts support
- 📦 Organized modular structure

---

## 🛠️ Tech Stack

- Python
- PySide6 (Qt for Python)
- Scikit-learn (for model & vectorizer)

---

## 📁 Project Structure

```
SPAMDETECTOR/
│
├── main.py                # Entry point of the application
├── spamDetector.py       # Core spam detection logic
├── modelCreator.py       # Script to train the ML model
├── about.py              # About dialog window
│
├── model.pkl             # Trained ML model
├── vectorizer.pkl        # Text vectorizer
├── df.csv                # Dataset used for training
│
├── assets/
│   ├── fonts/            # Custom fonts used in UI
│   │   ├── Beautiful ES.ttf
│   │   ├── Cinzel-Bold.otf
│   │   ├── Cinzel-Regular.otf
│   │   ├── SpecialElite-Regular.ttf
│   │   └── VictorMono-Regular.ttf
│   │
│   └── sounds/           # Sound effects
│       ├── bg sound [Asher Fulero Ceremonial Library].mp3
│       ├── freesound_community-printer-scan-68679.wav
│       └── Printing.wav
│
└── __pycache__/
```

---

## ▶️ How to Run

```bash
git clone https://github.com/your-username/spam-detector.git
cd spam-detector
pip install -r requirements.txt
python main.py
```

---

## 📽️ Demo Video

[Video Link]

---

## 📸 Screenshot

![Blank Page UI](screenshots/blank%20page.png)

---

## 🙌 Credits

If you use this project or any part of it, please give credit:

**Jatin Verma**

**NOTE:** Do not use this project for **COMMERCIAL PURPOSES** without permission.

Assets:

- Fonts: Open-source fonts
- Sounds: Freesound & other free libraries

---

## 📜 License

This project is licensed under the MIT License.

---

## 🚀 Future Improvements

- Improve ML model accuracy
- Add real-time detection
- Enhance UI/UX
- Convert into a web application

---

## 💡 Note

This project was built for learning purposes to understand how real-world desktop applications and ML systems are structured.

---

## 🔥 Journey

This marks the first step in my journey toward building larger software systems and startups.
