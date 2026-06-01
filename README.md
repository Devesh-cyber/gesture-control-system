# 🖐️ Gesture Control System

Control your computer with hand gestures in real-time using just a webcam. No mouse. No keyboard. Just your hand.

![Python](https://img.shields.io/badge/Python-3.12-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.9-green)
![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10-orange)
![Platform](https://img.shields.io/badge/Platform-Linux-lightgrey)

---

## 📽️ Demo

<!-- After uploading your demo video to YouTube, replace the link below -->
[![Gesture Control System Demo](https://img.youtube.com/vi/YOUR_VIDEO_ID/0.jpg)](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

> Or watch directly: [YouTube Demo Link](https://www.youtube.com/watch?v=YOUR_VIDEO_ID)

---

## 🎮 Gestures

| Gesture | Action |
|---|---|
| ☝️ Index finger up | Move cursor |
| 🤏 Index + Middle pinch | Left click |
| 🤏 Index + Thumb pinch | Right click |
| ✊ Fist | Enter scroll mode |
| ✊ Fist move up | Scroll up |
| ✊ Fist move down | Scroll down |

---

## 🛠️ Tech Stack

- **Python 3.12**
- **OpenCV** — webcam feed, frame rendering, HUD overlays
- **MediaPipe** — real-time 21-point hand landmark detection
- **PyAutoGUI** — OS-level mouse control
- **NumPy** — coordinate math and smoothing

---

## ⚙️ Setup

**1. Clone the repo**
```bash
git clone https://github.com/Devesh-cyber/gesture-control-system.git
cd gesture-control-system
```

**2. Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Linux — install Xlib**
```bash
sudo apt install python3-xlib
```

**5. Run**
```bash
python3 main.py
```

Press `q` or `Esc` to quit.

---

## 🔧 Tuning

All parameters in `config/settings.py`:

```python
MOUSE_SMOOTHING_FACTOR = 0.07   # Lower = smoother
MOUSE_MARGIN           = 120    # Control zone border
CLICK_COOLDOWN_MS      = 350    # Min time between clicks
```

---

## 🗺️ Roadmap

- [x] Hand tracking with neon HUD
- [x] Cursor movement with EMA smoothing
- [x] Left click, right click
- [x] Fist scroll
- [ ] Volume control
- [ ] Brightness control
- [ ] Screenshot gesture
- [ ] Air keyboard
- [ ] Custom gesture training

---

## 👨‍💻 Author

**Devesh Kadam** — BCA Student, Mulund College of Commerce, Mumbai

[LinkedIn](https://linkedin.com/in/YOUR_PROFILE) • [GitHub](https://github.com/Devesh-cyber)
