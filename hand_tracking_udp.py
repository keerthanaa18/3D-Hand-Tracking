import cv2
from cvzone.HandTrackingModule import HandDetector
import socket

width, height = 1280, 720
cap = cv2.VideoCapture(0)
cap.set(3, width)
cap.set(4, height)

detector = HandDetector(maxHands=1, detectionCon=0.8)

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
serverAddressPort = ("127.0.0.2", 5032)

while True:
    success, img = cap.read()
    hands, img = detector.findHands(img)
    data = []
    if hands:
        hand = hands[0]
        lmList = hand['lmList']
        for lm in lmList:
            data.extend([lm[0], height - lm[1], lm[2]])  # Flip y for Unity
        sock.sendto(str.encode(str(data)), serverAddressPort)

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
