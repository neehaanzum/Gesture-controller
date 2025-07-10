def detect_fist(hand_landmarks):
    tip_ids = [4, 8, 12, 16, 20]
    folded = sum(hand_landmarks.landmark[i].y > hand_landmarks.landmark[i - 2].y for i in tip_ids)
    return folded >= 4  # Relaxed threshold

def detect_peace_sign(hand_landmarks):
    is_index_up = hand_landmarks.landmark[8].y < hand_landmarks.landmark[6].y
    is_middle_up = hand_landmarks.landmark[12].y < hand_landmarks.landmark[10].y
    is_ring_down = hand_landmarks.landmark[16].y > hand_landmarks.landmark[14].y
    is_pinky_down = hand_landmarks.landmark[20].y > hand_landmarks.landmark[18].y
    return is_index_up and is_middle_up and is_ring_down and is_pinky_down
