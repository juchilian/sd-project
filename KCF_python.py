import cv2
def frame_resize(frame,n=2):
    return cv2.resize(frame, (int(frame.shape[1]*2/3), int(frame.shape[0]*2/3)))

if __name__ == '__main__':
    tracker = cv2.TrackerKCF_create()
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FPS, 120)

    while True:
        ret, frame = cap.read()
        # if not ret:
        #     continue
        frame = frame_resize(frame)

        bbox = (0,0,10,10)
        bbox = cv2.selectROI(frame,False)
        ok = tracker.init(frame, bbox)
        cv2.destroyAllWindows()
        break

    while True:
        ret, frame = cap.read()
        if not ret:
            k = cv2.waitKey(1)
            if k == 27 :
                break
            continue

   
        timer = cv2.getTickCount()

  
        track, bbox = tracker.update(frame)


        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);


        if track:
   
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (0,255,0), 2, 1)
        else :
  
            cv2.putText(frame, "Failure", (10,50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA);


        cv2.putText(frame, "FPS : " + str(int(fps)), (10,20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1, cv2.LINE_AA);


        cv2.imshow("Tracking", frame)


        k = cv2.waitKey(1)
        if k == 27 :
            break

cap.release()
cv2.destroyAllWindows()