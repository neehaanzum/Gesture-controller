import cv2
import mediapipe as mp
import time
import pyautogui
from multiprocessing import Process, set_start_method
from youtube_launcher import open_youtube_video
from gesture_utils import detect_fist, detect_peace_sign
from ui_overlay import launch_overlay

def main():
    # Launch YouTube
    print("[INFO] Opening YouTube...")
    driver = open_youtube_video("https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    time.sleep(7)
    pyautogui.click(600, 400)

    # Setup webcam and MediaPipe
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(max_num_hands=1)
    cap = cv2.VideoCapture(0)
    cooldown = 2
    last_action_time = 0

    while True:
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)
        now = time.time()

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                if now - last_action_time > cooldown:
                    if detect_fist(hand_landmarks):
                        pyautogui.press('space')
                        print("[GESTURE] ✊ Fist → Play/Pause")
                        last_action_time = now

                    elif detect_peace_sign(hand_landmarks):
                        print("[GESTURE] ✌️ Peace → Auto Screenshot")
                        Process(target=launch_overlay, args=(True, 3), daemon=True).start()
                        last_action_time = now

        cv2.imshow("AirPointer - Gesture Controller", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    driver.quit()

if __name__ == "__main__":
    set_start_method('spawn')  # Needed for Windows multiprocessing
    main()
