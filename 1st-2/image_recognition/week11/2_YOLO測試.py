from ultralytics import YOLO
import cv2 #載入cv2
#設定視窗名稱及型態
cv2.namedWindow('YOLOv8', cv2.WINDOW_NORMAL)

model = YOLO('yolov8x.pt')  # 物件辨識模型
modelSeg = YOLO('yolov8x-seg.pt')  # 物件分割模型
modelPose = YOLO('yolov8x-pose.pt')  # 身體姿態模型

#顯示物件列表
names=model.names

#讀取影像
frame=cv2.imread('road.jpg')

#進行辨識
results = model.predict(frame,verbose=False)
# results = modelSeg.predict(frame,verbose=False)
# results = modelPose.predict(frame,verbose=False)


item_count = {}
for data in results[0].boxes.data:
    x1 = int(data[0])
    x2 = int(data[1])
    y1 = int(data[2])
    y2 = int(data[3])
    r = round(float(data[4]), 2)
    n = names[int(data[5])]
    if n in item_count:
        item_count[n] += 1
    else:
        item_count[n] = 1
    print(x1,x2,y1,y2,r,n)

print("-"*30)
for i in item_count:
    print(f"{i} : {item_count[i]}")

#畫出辨識結果
frame = results[0].plot()
cv2.imshow('YOLOv8',frame)
key=cv2.waitKey(0) #使用者按了鍵盤
