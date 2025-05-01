import cv2
import mediapipe as mp
import pyautogui
import math
import threading
from enum import Enum

class Gesture(Enum):
    OPEN_HAND = 1
    POINTING = 2
    CLOSED_FIST = 3
    THUMBS_UP = 4
    THUMBS_DOWN = 5

class HandGestureController:
    def __init__(self, ui_controller):
        self.ui_controller = ui_controller
        self.cap = cv2.VideoCapture(0)
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.running = False
        self.last_gesture = None
        self.gesture_threshold = 10  # frames to confirm gesture
        self.gesture_counter = 0
        self.screen_width, self.screen_height = pyautogui.size()
        
    def start(self):
        self.running = True
        thread = threading.Thread(target=self._run_gesture_loop)
        thread.daemon = True
        thread.start()
        
    def stop(self):
        self.running = False
        self.cap.release()
        
    def _run_gesture_loop(self):
        while self.running:
            success, img = self.cap.read()
            if not success:
                continue
                
            img = cv2.flip(img, 1)
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.hands.process(img_rgb)
            
            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:
                    self.mp_draw.draw_landmarks(
                        img, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                    
                    current_gesture = self._recognize_gesture(hand_landmarks)
                    self._handle_gesture(current_gesture)
                    
                    # Draw gesture info on screen
                    cv2.putText(img, f"Gesture: {current_gesture}", 
                               (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 
                               1, (255, 0, 0), 2)
            
            cv2.imshow("Hand Gesture Control", img)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
                
        cv2.destroyAllWindows()
        
    def _recognize_gesture(self, landmarks):
        thumb_tip = landmarks.landmark[4]
        index_tip = landmarks.landmark[8]
        middle_tip = landmarks.landmark[12]
        ring_tip = landmarks.landmark[16]
        pinky_tip = landmarks.landmark[20]
        wrist = landmarks.landmark[0]
        
        # Calculate distances between fingertips and wrist
        thumb_dist = self._distance(thumb_tip, wrist)
        index_dist = self._distance(index_tip, wrist)
        middle_dist = self._distance(middle_tip, wrist)
        ring_dist = self._distance(ring_tip, wrist)
        pinky_dist = self._distance(pinky_tip, wrist)
        
        # Gesture recognition logic
        if (index_dist > 0.2 and middle_dist < 0.1 and 
            ring_dist < 0.1 and pinky_dist < 0.1):
            return Gesture.POINTING
            
        elif (thumb_dist > 0.2 and index_dist > 0.2 and 
              middle_dist > 0.2 and ring_dist > 0.2 and pinky_dist > 0.2):
            return Gesture.OPEN_HAND
            
        elif (thumb_dist < 0.1 and index_dist < 0.1 and 
              middle_dist < 0.1 and ring_dist < 0.1 and pinky_dist < 0.1):
            return Gesture.CLOSED_FIST
            
        elif (thumb_dist > 0.2 and index_dist < 0.1 and 
              middle_dist < 0.1 and ring_dist < 0.1 and pinky_dist < 0.1):
            return Gesture.THUMBS_UP
            
        elif (thumb_dist < 0.1 and index_dist > 0.2 and 
              middle_dist < 0.1 and ring_dist < 0.1 and pinky_dist < 0.1):
            return Gesture.THUMBS_DOWN
            
        return None
        
    def _distance(self, point1, point2):
        return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)
        
    def _handle_gesture(self, gesture):
        if gesture == self.last_gesture:
            self.gesture_counter += 1
        else:
            self.gesture_counter = 0
            self.last_gesture = gesture
            
        if self.gesture_counter >= self.gesture_threshold:
            if gesture == Gesture.OPEN_HAND:
                self.ui_controller.toggle_sidebar()
            elif gesture == Gesture.POINTING:
                self.ui_controller.navigate_next()
            elif gesture == Gesture.CLOSED_FIST:
                self.ui_controller.navigate_previous()
            elif gesture == Gesture.THUMBS_UP:
                self.ui_controller.confirm_selection()
            elif gesture == Gesture.THUMBS_DOWN:
                self.ui_controller.cancel_selection()
                
            self.gesture_counter = 0