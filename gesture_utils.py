import numpy as np

def count_fingers(lm_list):
    """
    Counts the number of fingers extended based on landmark positions.
    """
    tip_ids = [4, 8, 12, 16, 20]  # Thumb, Index, Middle, Ring, Pinky
    fingers = []

    # Thumb: compare x positions
    if lm_list[tip_ids[0]][1] > lm_list[tip_ids[0] - 1][1]:
        fingers.append(1)
    else:
        fingers.append(0)

    # Fingers: compare y positions
    for id in range(1, 5):
        if lm_list[tip_ids[id]][2] < lm_list[tip_ids[id] - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)

    return fingers.count(1)

def get_hand_position(lm_list, img_width, img_height):
    """
    Returns the general position of the hand: 'left', 'right', 'up', 'down', 'center'
    """
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