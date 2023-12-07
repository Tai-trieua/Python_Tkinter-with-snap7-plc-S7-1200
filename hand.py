#=======================================================
#==================Hand Module==========================

import time
import cv2
import mediapipe as map

#=======================================================
#======================class hand=======================
class handDetector():
    def __init__(self, mode = False, maxHands = 2, detectionCon = 0.5, trackCon =0.5):
        self.mode = mode
        self.maxHands = maxHands
        self.detectionCon = detectionCon
        self.trackCon = trackCon
        self.mpHands = map.solutions.hands
        self.hands = self.mpHands.Hands(self.mode, self.maxHands, self.detectionCon, self.trackCon)
        self.mpDraw = map.solutions.drawing_utils
        #self.draw = self.mpDraw.DrawingSpec(thickness=1, circle_radius=1)
        #self.mpDraw.draw_landmarks(self.img, self.results.multi_hand_landmarks, self.draw, self.mpHands.HAND_CONNECTIONS)
    
    def findHands(self,img, draw = True):
        imgRGB = cv2.cvtColor(img,cv2.COLOR_BGRA2RGB)
        self.result = self.hands.process(imgRGB)
        
        if self.result.multi_hand_landmarks:
            for handLms in self.result.multi_hand_landmarks:
                if draw:
                    self.mpDraw.draw_landmarks(img, handLms, self.mpDraw.HAND_CONNECTIONS)
        return img
    
    def findPosition(self, img, handNo =0, draw = True):
        lmlist =[]
        if self.result.multi_hand_landmarks:
            myHand = self.result.multi_hand_landmarks[handNo]
            for id, lm in enumerate(myHand.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)
        return lmlist
    
def main():
    pTime =0
    cTime =0
    cap = cv2.VideoCapture(1)
    detector = handDetector()
    while True:
        success, img = cap.read()
        img = detector.findHands(img)
        lmlist = detector.findPosition(img)
        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv2.putText(img, "FPS: {:.2f}".format(fps), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.imshow("img", img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

if __name__=='__main__':
    main()    