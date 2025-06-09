import numpy as np

def count_fingers(lm_list):
    tip_ids = [4, 8, 12, 16, 20]  
    fingers = []


    if lm_list[tip_ids[0]][1] > lm_list[tip_ids[0] - 1][1]:
        fingers.append(1)
    else:
        fingers.append(0)


    for id in range(1, 5):
        if lm_list[tip_ids[id]][2] < lm_list[tip_ids[id] - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)

def get_hand_position(lm_list, img_width, img_height):

    cx = int(np.mean([pt[1] for pt in lm_list]))
    cy = int(np.mean([pt[2] for pt in lm_list]))

    margin_x = img_width // 3
    margin_y = img_height // 3

    if cx < margin_x:
        return 'left'
    elif cx > 2 * margin_x:
        return 'right'
    elif cy < margin_y:
        return 'up'
    elif cy > 2 * margin_y:
        return 'down'
    else:
        return 'center'

def detect_fingers_up(lm_list):
    tip_ids = [4, 8, 12, 16, 20]
    finger_up = {
        "thumb" : 0,
        "index" : 0,
        "middle" : 0,
        "ring" : 0,
        "pinky" : 0 
    }

    if lm_list[tip_ids[0]][1] > lm_list[tip_ids[0] - 1][1]:
        finger_up['thumb'] = 1

    fingers = ["index", "middle", "ring", "pinky"]

    for i in range(1, 5):
        if lm_list[tip_ids[i]][2] < lm_list[tip_ids[i] - 2][2]:
            finger_up[fingers[i - 1]] = 1

    return finger_up