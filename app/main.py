import cv2
import time
from collections import deque

from utils.hand_detector import HandDetector
from utils.gesture_classifier import GestureClassifier
from utils.speech import Speaker
from gestures.gesture_map import GESTURE_TO_TEXT


def main():
    print("Starting Mute Child Gesture System...")

    # 🔴 Try camera index 0
    cap = cv2.VideoCapture(0)

    # If camera 0 fails, try camera 1
    if not cap.isOpened():
        print("Camera 0 not found, trying camera 1...")
        cap = cv2.VideoCapture(1)

    if not cap.isOpened():
        print("❌ ERROR: No camera detected")
        return

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    detector = HandDetector()
    classifier = GestureClassifier()
    speaker = Speaker()

    gesture_buffer = deque(maxlen=7)
    stable_gesture = None
    last_spoken_gesture = None
    last_spoken_time = 0

    print("Camera started successfully. Press Q to quit.")

    while True:
        ret, frame = cap.read()
        if not ret:
            print("⚠️ Frame not received from camera")
            continue

        frame, landmarks = detector.find_hand(frame)
        gesture = classifier.classify(landmarks)

        if gesture:
            gesture_buffer.append(gesture)

        if len(gesture_buffer) == gesture_buffer.maxlen:
            stable_gesture = max(set(gesture_buffer), key=gesture_buffer.count)

        current_time = time.time()

        if (
            stable_gesture
            and stable_gesture != last_spoken_gesture
            and (current_time - last_spoken_time) > 1.5
        ):
            text = GESTURE_TO_TEXT.get(stable_gesture, "")
            if text and not speaker.is_speaking:
                speaker.speak(text)
                last_spoken_gesture = stable_gesture
                last_spoken_time = current_time
                gesture_buffer.clear()

        if stable_gesture:
            cv2.putText(
                frame,
                f"Gesture: {stable_gesture}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2
            )

        cv2.imshow("Mute Child Gesture to Speech", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        time.sleep(0.02)

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
