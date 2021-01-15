import cv2
import numpy as np
import time

class Kcf_python():  
    def __init__(self):
        self.tracker = cv2.TrackerKCF_create()
        self.cap = cv2.VideoCapture(0)
        self.value = 1
        self.time_value = 0
        self.re_time1 = 0

    def frame_resize(self,frame,n=2):
        return cv2.resize(frame, (int(frame.shape[1]*1/2), int(frame.shape[0]*1/2)))

    def key_decide(self,x,threshold):
        K_LEFT=0
        K_RIGHT=0
        if x < threshold/3:
            K_RIGHT = 1
        if x > threshold*2/3:
            K_LEFT=1
        return [K_RIGHT,K_LEFT]

    #一枚の写真を撮影してバウンディングボックスを作成
    def make_bbox(self):
        #webカメラ取り込み
        ret, frame = self.cap.read()
        #選択した部分をBounding Boxとする
        bbox = cv2.selectROI(windowName="Make Bounding Box", img = frame,showCrosshair=False, fromCenter=False)
        self.tracker.init(frame, bbox)
        cv2.destroyAllWindows()

    def tracking_face(self,game):
        ret, frame = self.cap.read()
        track, bbox = self.tracker.update(frame)
        fps = cv2.CAP_PROP_FPS
        [K_RIGHT, K_LEFT] = [0,0]

        if track:
            #p1が左上の点、つまりbboxは
            #bbox = [x座標,y座標,x軸方向での変位,y軸方向での変位]
            threshold = frame.shape[1]#閾値はウィンドウサイズが基準
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (0,255,0), 2, 1)
            bbox_center_x = int(bbox[0] + 1/2*bbox[2])
            #キー操作の値を変数に入れてる
            K_RIGHT, K_LEFT = self.key_decide(bbox_center_x,threshold)
            self.value = 1
            self.time_value = 0
            game.re_elapsed_time = 0

            
    
        else :
            self.value = 0
            if self.time_value == 0:
                self.re_time1 = time.time()
                self.time_value = 1
            cv2.putText(frame, "Failure", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
            [K_RIGHT, K_LEFT] = [0,0]

        
        cv2.putText(frame, "FPS : " + str(int(fps)), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA)
        frame = np.array(frame)
        frame = np.fliplr(frame)
        cv2.imshow("Tracking", frame)
        return [K_RIGHT, K_LEFT]


# if __name__ == '__main__':
#     kcf = Kcf_python()
#     kcf.make_bbox()
#     while True:
#         print(kcf.tracking_face())#make_bboxは最初の写真#tracking_faceは後のどうがの部分
#         k = cv2.waitKey(1)
#         if k == 27 :
#             break
