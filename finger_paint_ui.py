import cv2
import mediapipe as mp
import datetime
import random

# Setup MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
canvas = None
drawing_enabled = False
drawing_active = True
brush_color = (255, 0, 255)
brush_color_name = "Purple"
brush_size = 8
brush_type = "Circle"  # Circle, Square, Spray
shape_mode = "Free"    # Free, Line, Rect, CircleS
shape_start = None

# Button layout
buttons = [
    {'pos': (10, 60), 'size': (60, 60), 'color': (255, 0, 255), 'label': 'Purple'},
    {'pos': (80, 60), 'size': (60, 60), 'color': (0, 255, 0), 'label': 'Green'},
    {'pos': (150, 60), 'size': (60, 60), 'color': (0, 255, 255), 'label': 'Yellow'},
    {'pos': (220, 60), 'size': (60, 60), 'color': (255, 0, 0), 'label': 'Blue'},
    {'pos': (290, 60), 'size': (60, 60), 'color': (255, 255, 255), 'label': 'Eraser'},
    {'pos': (360, 60), 'size': (60, 60), 'color': (0, 0, 0), 'label': 'Clear'},
    {'pos': (430, 60), 'size': (60, 60), 'color': (200, 200, 200), 'label': '+'},
    {'pos': (500, 60), 'size': (60, 60), 'color': (200, 200, 200), 'label': '-'},
    {'pos': (570, 60), 'size': (100, 60), 'color': (150, 150, 150), 'label': 'Draw'},
    {'pos': (680, 60), 'size': (100, 60), 'color': (100, 255, 100), 'label': 'Save'},
    {'pos': (10, 130), 'size': (100, 40), 'color': (100, 100, 255), 'label': 'Circle'},
    {'pos': (120, 130), 'size': (100, 40), 'color': (100, 100, 255), 'label': 'Square'},
    {'pos': (230, 130), 'size': (100, 40), 'color': (100, 100, 255), 'label': 'Spray'},
    {'pos': (340, 130), 'size': (80, 40), 'color': (255, 100, 100), 'label': 'Line'},
    {'pos': (430, 130), 'size': (100, 40), 'color': (255, 100, 100), 'label': 'Rect'},
    {'pos': (540, 130), 'size': (100, 40), 'color': (255, 100, 100), 'label': 'CircleS'},
    {'pos': (650, 130), 'size': (100, 40), 'color': (150, 150, 255), 'label': 'Free'},
]

def is_inside_button(finger_pos, button):
    x, y = button['pos']
    w, h = button['size']
    fx, fy = finger_pos
    return x <= fx <= x + w and y <= fy <= y + h

def is_fist(landmarks):
    fingers_folded = 0
    finger_tips = [8, 12, 16, 20]
    finger_dips = [6, 10, 14, 18]
    for tip, dip in zip(finger_tips, finger_dips):
        if tip in landmarks and dip in landmarks:
            if landmarks[tip][1] > landmarks[dip][1]:
                fingers_folded += 1
    return fingers_folded == 4

def draw_brush(canvas, pos, color, size, style):
    if style == "Circle":
        cv2.circle(canvas, pos, size, color, -1)
    elif style == "Square":
        x, y = pos
        cv2.rectangle(canvas, (x - size, y - size), (x + size, y + size), color, -1)
    elif style == "Spray":
        for _ in range(20):
            dx = random.randint(-size, size)
            dy = random.randint(-size, size)
            if dx*dx + dy*dy <= size*size:
                cv2.circle(canvas, (pos[0]+dx, pos[1]+dy), 1, color, -1)

while cap.isOpened():
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    if canvas is None:
        canvas = frame.copy() * 0

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(rgb)

    index_pos = None
    landmarks = {}

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, handLms, mp_hands.HAND_CONNECTIONS)
            for i, lm in enumerate(handLms.landmark):
                landmarks[i] = (int(lm.x * w), int(lm.y * h))
            index_pos = landmarks.get(8)
            drawing_active = not is_fist(landmarks)

            if drawing_enabled and drawing_active and index_pos and index_pos[1] > 180:
                if shape_mode == "Free":
                    draw_brush(canvas, index_pos, brush_color, brush_size, brush_type)
                elif shape_start is None:
                    shape_start = index_pos
                else:
                    if shape_mode == "Line":
                        cv2.line(canvas, shape_start, index_pos, brush_color, brush_size)
                    elif shape_mode == "Rect":
                        cv2.rectangle(canvas, shape_start, index_pos, brush_color, brush_size)
                    elif shape_mode == "CircleS":
                        radius = int(((shape_start[0]-index_pos[0])**2 + (shape_start[1]-index_pos[1])**2)**0.5)
                        cv2.circle(canvas, shape_start, radius, brush_color, brush_size)
                    shape_start = None

    if index_pos:
        for btn in buttons:
            if is_inside_button(index_pos, btn):
                label = btn['label']
                if label == 'Clear':
                    canvas = frame.copy() * 0
                elif label == '+':
                    brush_size = min(brush_size + 2, 50)
                elif label == '-':
                    brush_size = max(brush_size - 2, 2)
                elif label == 'Draw':
                    drawing_enabled = not drawing_enabled
                elif label == 'Eraser':
                    brush_color = (255, 255, 255)
                    brush_color_name = "Eraser"
                    brush_size = 30
                elif label == 'Save':
                    filename = f"drawing_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                    output = cv2.addWeighted(frame, 0.5, canvas, 1, 0)
                    cv2.imwrite(filename, output)
                    print(f"📸 Saved: {filename}")
                elif label in ["Circle", "Square", "Spray"]:
                    brush_type = label
                elif label in ["Line", "Rect", "CircleS", "Free"]:
                    shape_mode = label
                    shape_start = None
                else:
                    brush_color = btn['color']
                    brush_color_name = label
                    brush_size = 8

    # Draw UI buttons
    for btn in buttons:
        x, y = btn['pos']
        w_, h_ = btn['size']
        color = btn['color']
        cv2.rectangle(frame, (x, y), (x + w_, y + h_), color, -1)
        cv2.rectangle(frame, (x, y), (x + w_, y + h_), (0, 0, 0), 2)
        cv2.putText(frame, btn['label'], (x + 5, y + h_ - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 2)

    combined = cv2.addWeighted(frame, 1, canvas, 1, 0)
    status = f"{brush_type} Brush | Size: {brush_size}px | Shape: {shape_mode} | Drawing: {'ON' if drawing_enabled and drawing_active else 'OFF'}"
    cv2.putText(combined, status, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, brush_color, 2)

    cv2.imshow("🖐️ Finger Paint Pro", combined)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()