import cv2
import mediapipe as mp

class HandDetector:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.draw = mp.solutions.drawing_utils

    def find_hand(self, frame):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = self.hands.process(rgb)

        landmarks = []

        if result.multi_hand_landmarks:
            for hand in result.multi_hand_landmarks:
                self.draw.draw_landmarks(
                    frame, hand, self.mp_hands.HAND_CONNECTIONS
                )
                for lm in hand.landmark:
                    landmarks.append((lm.x, lm.y))
        return frame, landmarks
