# cap = cv2.VideoCapture(0)

# while True:
#     ret,frame = cap.read()
#     if ret == False:
#         print("Can't recognize camera")

# frame = cv2.imread("/Users/toshikifukui/Desktop/sd-project/img/car_3.png")
# gray = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
# sift = cv2.SIFT()
# kp = sift.detect(gray,None)

# img=cv2.drawKeypoints(gray,kp)
# cv2.imwrite("fujiishine.jpg",img)

# cv2.imshow("frame",img)
# if cv2.waitKey(1)&0xFF == ord('q'):
#     break
        
# cap.release()
# cv2.destroyAllWindows()

# import cv2
# import numpy as np

# img = cv2.imread('/Users/toshikifukui/Desktop/宇宙×衣食住.png')
# gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

# sift = cv2.SIFT()
# kp = sift.detect(gray,None)

# img=cv2.drawKeypoints(gray,kp)

# cv2.imwrite('fujiishine.jpg',img)

# 大っ嫌い！！

import cv2
img = cv2.imread('/Users/toshikifukui/Downloads/news_300404_1.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
sift = cv2.SIFT_create()
kp = sift.detect(gray,None)
img=cv2.drawKeypoints(gray,kp,outImage = None)
# img=cv2.drawKeypoints(gray,kp,flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
cv2.imwrite('fujiishine.jpg',img)
