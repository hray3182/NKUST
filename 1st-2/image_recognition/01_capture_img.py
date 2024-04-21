import cv2

# 選擇第1隻攝影機
cap = cv2.VideoCapture(1)
i = 0
while cap.isOpened():
    # 從攝影機擷取一張影像
    ret, frame = cap.read()  # ret=retval,frame=image
    # 顯示圖片
    cv2.imshow("frame", frame)
    frame = cv2.resize(frame, (200, 200))
    i += 1
    if i % 2 == 0:
        cv2.imwrite("train/R/" + str(i) + ".jpg", frame)
        print("Save photo:" + str(i) + ".jpg")
    if i > 200:
        exit()

    key = cv2.waitKey(1)
    # 按q離開
    if key & 0xFF == ord("q"):
        break

# 釋放攝影機
cap.release()

# 關閉所有 OpenCV 視窗
cv2.destroyAllWindows()
