import cv2
import sys
import traceback
import numpy as np
import matplotlib.pyplot as plt
import time

cap = cv2.VideoCapture(0)
cascade = cv2.CascadeClassifier("/Users/toshikifukui/画像処理-OpenCV/haarcascade_frontalface_alt2.xml")
cap.set(cv2.CAP_PROP_FPS, 120)
fps = cv2.CAP_PROP_FPS

time = 0

try:
    while True:
        ret, frame = cap.read()
        facereac = cascade.detectMultiScale(frame)

        if ret == False:
            print("Couldn't recognise camera")
            continue
        
        frame = np.array(frame)

        value_g = []

        if len(facereac) > 0:
            for rect in facereac:
#                 mag = 3
#                 x = int(x*mag)
#                 width = int(width*mag)
#                 height = int(height*mag)
                cv2.rectangle(frame, tuple(rect[0:2]), tuple(rect[0:2]+rect[2:4]), (0,255,255), 1)
                # print(tuple(rect[0:2])[0])
                #新たな画像の定義
                frame_new = frame[tuple(rect[0:2])[0]:tuple(rect[0:2]+rect[2:4])[0], tuple(rect[0:2])[1]:tuple(rect[0:2]+rect[2:4])[1]]
                frame_new = np.array(frame_new)
                # print(frame_new)
                # print(frame_new.shape)
                # data_all = 0

                #画像内部からGデータを抽出
                # print(frame_new.shape)
                # for index in range(frame_new.shape[0]):
                #     for column in range(frame_new.shape[1]):
                #         data_all += (frame_new[index][column][1])
                #ここ！
                # if frame_new.shape[0] != 0 and frame_new.shape[1] != 0:
                #     average_score = data_all / (frame_new.shape[0]*frame_new.shape[1])
                # print(average_score)
                # time += 1/num_fps
                # plt.plot(time,average_score,marker = "o",color = "b")
                # plt.pause(1/num_fps)
                
                        # グラフをクリア
                timer = cv2.getTickCount()
                fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
                cv2.putText(frame, "FPS : " + str(int(fps)), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA);
                cv2.putText(frame, "Person", (100, 100), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 255),3)
            
        cv2.imshow("frame", frame)
        
        if cv2.waitKey(1)&0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
    
except:
    print("Error", sys.exc_info()[0])
    print(sys.exc_info()[1])
    print(traceback.format_tb(sys.exc_info()[2]))
