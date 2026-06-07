import cv2
import mediapipe as mp
import numpy as np
from datetime import datetime

# =========================
# Camera
# =========================
cap = cv2.VideoCapture(0)

# =========================
# MediaPipe Setup
# =========================
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

# =========================
# Variables
# =========================
canvas = None

prev_x = None
prev_y = None

smooth_x = 0
smooth_y = 0

drawing = False
eraser = False

brush_size = 10

# Colors (BGR)
colors = {
    1: (255, 0, 255),    # Bright Purple
    2: (0, 255, 0),      # Bright Green
    3: (255, 100, 0),    # Orange
    4: (0, 0, 255),      # Bright Red
    5: (255, 255, 0),    # Cyan
    6: (255, 255, 255)   # White
}

current_color = colors[1]
color_index = 1

import time
last_color_change = 0
first_start_time = None

# =========================
# Main Loop
# =========================
while True:

    success, img = cap.read()

    if not success:
        break

    img = cv2.flip(img, 1)

    h, w, c = img.shape

    if canvas is None:
        canvas = np.zeros((h, w, 3), dtype=np.uint8)

    rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    if results.multi_hand_landmarks:

        for hand_landmarks in results.multi_hand_landmarks:

            mp_draw.draw_landmarks(
                img,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS
            )

            tips = [4, 8, 12, 16, 20]

            fingers = []

            # Thumb
            if hand_landmarks.landmark[4].x < hand_landmarks.landmark[3].x:
                fingers.append(1)
            else:
                fingers.append(0)

            # Other fingers
            for tip_id in tips[1:]:

                if hand_landmarks.landmark[tip_id].y < hand_landmarks.landmark[tip_id - 2].y:
                    fingers.append(1)
                else:
                    fingers.append(0)


            # Index fingertip
            tip = hand_landmarks.landmark[8]

            index_x = int(tip.x * w)
            index_y = int(tip.y * h)

            # Smooth movement
            smooth_x = int(0.7 * smooth_x + 0.3 * index_x)
            smooth_y = int(0.7 * smooth_y + 0.3 * index_y)

            index_x = smooth_x
            index_y = smooth_y

            # Cursor
            cv2.circle(
                img,
                (index_x, index_y),
                12,
                (0, 255, 0),
                cv2.FILLED
            )

            if drawing:

                if prev_x is not None and prev_y is not None:

                    cv2.line(
                        canvas,
                        (prev_x, prev_y),
                        (index_x, index_y),
                        current_color,
                        brush_size
                    )

            if eraser:

                cv2.circle(
                    canvas,
                    (index_x, index_y),
                    30,
                    (0, 0, 0),
                    -1
                )

            prev_x = index_x
            prev_y = index_y

            if fingers == [0, 1, 0, 0, 0]:
                drawing = True
                eraser = False

            if fingers == [0, 1, 1, 0, 0]:
                drawing = False
                eraser = False

            if fingers == [0, 1, 1, 1, 0]:

                drawing = False
                eraser = False

                current_time = time.time()

                if current_time - last_color_change > 1.5:

                    color_index += 1

                    if color_index > len(colors):
                        color_index = 1

                    current_color = colors[color_index]
                    print("COLOR CHANGED TO:", color_index)
                    last_color_change = current_time
            # Open palm = clear screen

            if fingers == [1, 1, 1, 1, 1]:
                cv2.putText(
                    img,
                    "CLEARING...",
                    (20, 200),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 255, 255),
                    2
                )

                canvas[:] = 0
            # Closed fist = eraser

            if fingers == [0, 0, 0, 0, 0]:

                if fist_start_time is None:
                    fist_start_time = time.time()

                elif time.time() - fist_start_time > 1:

                    drawing = False
                    eraser = True

            else:
                fist_start_time = None

                cv2.putText(
                    img,
                    "ERASER",
                    (20, 160),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2
                )

    # Merge drawing layer
    final_img = cv2.addWeighted(img, 1, canvas, 1, 0)

    # =========================
    # UI
    # =========================

    mode_text = "MOVE"

    if drawing:
        mode_text = "DRAWING"

    if eraser:
        mode_text = "ERASER"

    cv2.putText(
        final_img,
        f"MODE: {mode_text}",
        (20, 90),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (0, 255, 255),
        2
    )

    cv2.putText(
        final_img,
        f"BRUSH: {brush_size}",
        (20, 130),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8,
        (255, 255, 255),
        2
    )

    cv2.putText(
        final_img,
        "D=Draw  E=Erase  C=Clear  S=Save",
        (20, h - 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.putText(
        final_img,
        "1=Purple 2=Green 3=Blue 4=Red",
        (20, h - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    if results.multi_hand_landmarks:
        cv2.putText(
            final_img,
            f"FINGERS: {sum(fingers)}",
            (20, 170),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (255, 255, 255),
            2
        )
    cv2.rectangle(
        final_img,
        (w - 120, 10),
        (w - 20, 50),
        current_color,
        -1
    )

    cv2.putText(
        final_img,
        "COLOR",
        (w - 120, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )

    cv2.putText(
        final_img,
        "AirInk AI",
        (20, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 255),
        3
    )
    cv2.imshow("Air Writing Pro", final_img)

    # =========================
    # Keyboard Controls
    # =========================

    key = cv2.waitKey(1) & 0xFF

    if key == 27:
        break

    # Toggle drawing
    if key == ord('d'):
        drawing = not drawing
        eraser = False

    # Toggle eraser
    if key == ord('e'):
        eraser = not eraser
        drawing = False

    # Clear screen
    if key == ord('c'):
        canvas[:] = 0

    # Save screenshot
    if key == ord('s'):

        filename = f"drawing_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"

        cv2.imwrite(filename, canvas)

        print(f"Saved: {filename}")

    # Color shortcuts
    if key == ord('1'):
        current_color = colors[1]

    if key == ord('2'):
        current_color = colors[2]

    if key == ord('3'):
        current_color = colors[3]

    if key == ord('4'):
        current_color = colors[4]

    # Brush size
    if key == ord('+') or key == ord('='):
        brush_size += 2

    if key == ord('-'):
        brush_size = max(2, brush_size - 2)

cap.release()
cv2.destroyAllWindows()