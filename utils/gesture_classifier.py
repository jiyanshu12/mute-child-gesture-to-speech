class GestureClassifier:
    def classify(self, landmarks):
        if not landmarks or len(landmarks) < 21:
            return None

        # finger tips
        thumb = landmarks[4]
        index = landmarks[8]
        middle = landmarks[12]
        ring = landmarks[16]
        pinky = landmarks[20]

        # finger base joints
        index_base = landmarks[5]
        middle_base = landmarks[9]
        ring_base = landmarks[13]
        pinky_base = landmarks[17]

        # finger up logic
        index_up = index[1] < index_base[1]
        middle_up = middle[1] < middle_base[1]
        ring_up = ring[1] < ring_base[1]
        pinky_up = pinky[1] < pinky_base[1]

        # ---------------- PRIORITY ORDER ----------------
        # THANK YOU → index + middle + ring UP, pinky DOWN
        if index_up and middle_up and ring_up and not pinky_up:
            return "THANKYOU"

        # HELLO → all fingers UP
        if index_up and middle_up and ring_up and pinky_up:
            return "HELLO"

        # YES → index + middle
        if index_up and middle_up and not ring_up and not pinky_up:
            return "YES"

        # NO → only index
        if index_up and not middle_up and not ring_up and not pinky_up:
            return "NO"

        # WATER → only pinky
        if pinky_up and not index_up and not middle_up:
            return "WATER"

        # HELP → fist
        if not index_up and not middle_up and not ring_up and not pinky_up:
            return "HELP"

        return None

