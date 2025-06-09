import cv2
import mediapipe as mp
import pyautogui
from gesture_utils import count_fingers, get_hand_position

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
_, frame = cap.read()
h, w, _ = frame.shape

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    result = hands.process(img_rgb)

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            # Extract landmark positions
            lm_list = []
            for id, lm in enumerate(hand_landmarks.landmark):
                cx, cy = int(lm.x * w), int(lm.y * h)
                lm_list.append((id, cx, cy))

            if lm_list:
                finger_count = count_fingers(lm_list)
                position = get_hand_position(lm_list, w, h)

                # Display on screen
                cv2.putText(img, f'Fingers: {finger_count}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.putText(img, f'Pos: {position}', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

                # Example control mapping
                if position == 'up':
                    pyautogui.press('up')
                elif position == 'down':
                    pyautogui.press('down')
                elif position == 'left':
                    pyautogui.press('left')
                elif position == 'right':
                    pyautogui.press('right')

                if finger_count == 1:
                    pyautogui.press('space')  # Jump
                elif finger_count == 5:
                    pyautogui.press('enter')  # Start / Confirm

    cv2.imshow("Hand Gesture Controller", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()