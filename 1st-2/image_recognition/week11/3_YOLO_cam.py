import cv2
from ultralytics import YOLO
#設定視窗名稱及型態
cv2.namedWindow('YOLOv8', cv2.WINDOW_NORMAL)
cap=cv2.VideoCapture(1)

model = YOLO('yolov8x.pt')   
names = model.names

while 1:
    r,frame=cap.read() #讀取一張影像

    results = model.predict(frame,verbose=False)
    for data in results[0].boxes.data:
        x1 = int(data[0])
        x2 = int(data[1])
        y1 = int(data[2])
        y2 = int(data[3])
        r = round(float(data[4]), 2)
        n = names[int(data[5])]

        print(x1,x2,y1,y2,r,n)

    
    cv2.imshow('YOLOv8',results[0].plot()) #顯示影像
    key=cv2.waitKey(1) #使用者按了鍵盤
    if key==27: #27代表鍵盤的ESC
        break   #退出迴圈
