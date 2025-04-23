# minesweeper-
new features will update soon
# 💣 PyQt5 Minesweeper Game

A classic Minesweeper game built using PyQt5 in Python. Reveal all safe cells to win, and use logical deduction to avoid the mines!

---

## 🖥️ Features

- GUI built with PyQt5
- Timer and score tracking
- Restart button
- Flag mines with right-click
- Random mine generation

---

## 📦 Requirements

- Python 3.7+
- PyQt5
- PyInstaller (for building the `.exe`)

Install dependencies:

```bash
pip install pyqt5 pyinstaller

🔨 Build a Windows Executable
To create a .exe file:

Make sure pyinstaller is installed.

Use the included batch file to auto-build:

Double-click: build_minesweeper.bat

Or run from terminal:

bash
Copy
Edit
build_minesweeper.bat
This will:

Clean previous builds

Compile a fresh .exe

Save it to the dist/ folder

📁 File Structure
bash
Copy
Edit
/your-project/
│
├── minesweeper.py             # Main game code
├── build_minesweeper.bat      # Auto-build script for Windows
├── README.md                  # This file
├── dist/                      # Final .exe output
└── build/                     # PyInstaller temp files
📌 Gameplay Tip
The number on each revealed tile tells you how many mines are around it. Win by revealing all non-mine cells!

📃 License
MIT License — free to use, modify, and distribute.


