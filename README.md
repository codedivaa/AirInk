# AirInk AI

### Hand Gesture Based Virtual Writing System using OpenCV and MediaPipe

AirInk AI is a computer vision project that allows users to write in the air using hand gestures captured through a webcam. The system tracks hand landmarks in real time and converts finger movements into digital strokes on a virtual canvas.

---

## Features

* Real-time hand tracking
* Air writing using index finger
* Gesture-based interaction
* Multiple brush colors
* Eraser mode
* Canvas clearing
* Screenshot saving
* Adjustable brush size
* Live finger detection
* Smooth cursor tracking

---

## Technologies Used

* Python
* OpenCV
* MediaPipe
* NumPy

---

## System Architecture

```text
                Webcam Feed
                      │
                      ▼
                OpenCV Capture
                      │
                      ▼
             MediaPipe Hand Tracking
                      │
                      ▼
          Hand Landmark Detection
                      │
                      ▼
             Gesture Recognition
                      │
      ┌───────────────┼───────────────┐
      │               │               │
      ▼               ▼               ▼
   Drawing       Color Change      Eraser
   Module           Module         Module
      │               │               │
      └───────────────┼───────────────┘
                      │
                      ▼
                Canvas Renderer
                      │
                      ▼
                Display Output
                      │
                      ▼
              Screenshot Storage
```

---

## Workflow

1. Webcam captures live video.
2. OpenCV processes each frame.
3. MediaPipe detects hand landmarks.
4. Finger positions are analyzed.
5. Gestures are recognized.
6. Corresponding actions are executed.
7. The drawing is rendered on a virtual canvas.
8. Screenshots can be saved locally.

---

## Gesture Controls

| Gesture          | Action       |
| ---------------- | ------------ |
| ☝️ Index Finger  | Drawing Mode |
| ✌️ Two Fingers   | Move Cursor  |
| 🤟 Three Fingers | Change Color |
| ✋ Open Palm      | Clear Canvas |
| 👊 Closed Fist   | Eraser Mode  |

---

## Keyboard Controls

| Key | Action              |
| --- | ------------------- |
| S   | Save Screenshot     |
| C   | Clear Canvas        |
| 1   | Purple Color        |
| 2   | Green Color         |
| 3   | Orange Color        |
| 4   | Red Color           |
| +   | Increase Brush Size |
| -   | Decrease Brush Size |
| ESC | Exit Application    |

---

## Project Structure

```text
AirInk-AI/
│
├── main.py
├── README.md
├── requirements.txt
├── .gitignore
│
└── screenshots/
```

---

## Future Enhancements

* Handwriting to text conversion (OCR)
* Multi-hand support
* Shape recognition
* Gesture-based brush size control
* Whiteboard mode
* Cloud storage integration
* AI-powered handwriting beautification

---

## Screenshots

Save screenshots using the **S** key.

Example:

```text
screenshots/
├── drawing_20260607_183500.png
├── drawing_20260607_184200.png
```

---

## Author

Vaibhavi

AirInk AI – Hand Gesture Based Virtual Writing System
