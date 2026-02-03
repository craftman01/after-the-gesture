import cv2
import mediapipe as mp
import math
from pythonosc import udp_client

# ---------------- OSC ----------------
client = udp_client.SimpleUDPClient("127.0.0.1", 7000)

# ---------------- MEDIAPIPE ----------------
mp_hands = mp.solutions.hands
mp_face = mp.solutions.face_mesh
mp_draw = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

face_mesh = mp_face.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True
)

# ---------------- CAMERA ----------------
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# ---------------- SMOOTHING ----------------
alpha = 0.2
smooth_x = 0.5
smooth_y = 0.5

# ---------------- STATE MEMORY ----------------
prev_gesture_active = 0

# ---------------- HELPERS ----------------
def clamp(value, min_val=0.0, max_val=1.0):
    return max(min_val, min(value, max_val))

def distance(p1, p2):
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

# ---------------- MAIN LOOP ----------------
while True:
    success, frame = cap.read()
    if not success:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    hand_result = hands.process(rgb)
    face_result = face_mesh.process(rgb)

    raw_x = smooth_x
    raw_y = smooth_y
    ok_gesture = 0
    mouth_open = 0

    # ---------------- HAND ----------------
    if hand_result.multi_hand_landmarks:
        hand_landmarks = hand_result.multi_hand_landmarks[0]

        index_tip = hand_landmarks.landmark[8]
        thumb_tip = hand_landmarks.landmark[4]

        raw_x = clamp(index_tip.x)
        raw_y = clamp(index_tip.y)

        if distance(index_tip, thumb_tip) < 0.05:
            ok_gesture = 1

        mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # ---------------- SMOOTH ----------------
    smooth_x = smooth_x * (1 - alpha) + raw_x * alpha
    smooth_y = smooth_y * (1 - alpha) + raw_y * alpha

    # ---------------- MOUTH ----------------
    if face_result.multi_face_landmarks:
        face_landmarks = face_result.multi_face_landmarks[0]
        if abs(face_landmarks.landmark[13].y - face_landmarks.landmark[14].y) > 0.02:
            mouth_open = 1

    # ---------------- GESTURE LOGIC ----------------
    gesture_active = 1 if (ok_gesture == 1 and mouth_open == 1) else 0

    trigger = 0
    if gesture_active == 1 and prev_gesture_active == 0:
        trigger = 1  # RISING EDGE

    prev_gesture_active = gesture_active

    # ---------------- OSC ----------------
    client.send_message("/hand/x", smooth_x)
    client.send_message("/hand/y", smooth_y)
    client.send_message("/gesture/active", gesture_active)
    client.send_message("/gesture/trigger", trigger)

    # ---------------- DEBUG ----------------
    cv2.putText(frame, f"Gesture Active: {gesture_active}", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)
    cv2.putText(frame, f"TRIGGER: {trigger}", (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,0,255), 2)

    cv2.imshow("Gesture Logic Layer", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
