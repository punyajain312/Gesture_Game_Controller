import cv2
import mediapipe as mp
import pyautogui
from gesture_utils import count_fingers, get_hand_position, detect_fingers_up

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
                fingers_up = detect_fingers_up(lm_list)

                y_offset = 150
                for finger, is_up in fingers_up.items():
                    cv2.putText(img, f'{finger}: {"UP" if is_up else "DOWN"}', (10, y_offset), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
                    y_offset += 30
                if fingers_up["index"] and not fingers_up["middle"]:
                    pyautogui.press('w')  # Move forward
                elif fingers_up["middle"] and not fingers_up["index"]:
                    pyautogui.press('s')  # Move backward
                elif fingers_up["index"] and fingers_up["middle"]:
                    pyautogui.press('space')

                finger_count = count_fingers(lm_list)
                position = get_hand_position(lm_list, w, h)

                cv2.putText(img, f'Fingers: {finger_count}', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                cv2.putText(img, f'Pos: {position}', (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)


                # if position == 'up':
                #     pyautogui.press('up')
                # elif position == 'down':
                #     pyautogui.press('down')
                # elif position == 'left':
                #     pyautogui.press('left')
                # elif position == 'right':
                #     pyautogui.press('right')

                # if finger_count == 1:
                #     pyautogui.press('space')  # Jump
                # elif finger_count == 5:
                #     pyautogui.press('enter')  # Start / Confirm

    cv2.imshow("Hand Gesture Controller", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows() 