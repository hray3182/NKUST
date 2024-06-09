import cv2
from ultralytics import YOLO
import numpy as np

# 測試驗片 ./city.mp4
# model ./yolov8x.pt

def drawArea(f, area, color, th):
    for a in area:
        v = np.array(a, np.int32)
        cv2.polylines(f, [v], 1, color, th)

#設定視窗名稱及型態
cv2.namedWindow('YOLOv8', cv2.WINDOW_NORMAL)
cap=cv2.VideoCapture('assets/highway(tikva).mp4')

model = YOLO('yolov8x.pt')   

names = model.names

while 1:
    r,frame=cap.read() #讀取一張影像

    # results = model.predict(frame,verbose=False)
    # for data in results[0].boxes.data:
    #     print(type(data), data)
    #     x1 = int(data[0])
    #     x2 = int(data[1])
    #     y1 = int(data[2])
    #     y2 = int(data[3])
    #     r = round(float(data[4]), 2)
    #     n = names[int(data[5])]

    #     print(x1,x2,y1,y2,r,n)

    results = model.track(frame, persist=True, verbose=False)    
    for data in results[0].boxes.data:
        print(data)
        x1 = int(data[0])
        x2 = int(data[1])
        y1 = int(data[2])
        y2 = int(data[3])
        r = round(float(data[4]), 2)
        n = names[int(data[5])]

        if n in ['car', 'truck', 'bus']:
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
            # 寫上物件名與編號
            cv2.putText(frame, f"{n} {int(r*100)}%", (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)

    cv2.imshow('YOLOv8',frame) #顯示影像

    key=cv2.waitKey(1) #使用者按了鍵盤
    if key==27: #27代表鍵盤的ESC
        break   #退出迴圈
    
cap.release() #關閉攝影機

cv2.destroyAllWindows() #關閉視窗


