
import time
import os
import tensorflow as tf
import cv2
import numpy as np
#載入模型
model=tf.keras.models.load_model('RSP/CNN_RSP.keras')
size=(200,200)
data = np.ndarray(shape=(1, 200,200, 3), dtype=np.float32)
#取得類別標籤(用測試資料夾)
dirList = sorted(os.listdir("RSP/test/"))
cap = cv2.VideoCapture(1)#自行選擇攝影機編號
while cap.isOpened():
    start = time.time()
    ret, img = cap.read()
    frame=cv2.resize(img,(640,480))
    #處理陣列
    img = cv2.resize(img,(200,200))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  
    data[0]=np.asarray(img)/255
    #預測
    pr=model.predict(data)
    maxIndex = np.argmax(pr)#找出1,2,...0，機率最大的輸出
    maxPr=round(pr[0][maxIndex],3)
    #print(label) #印出所有機率
    if pr[0][maxIndex]>0.6:        
        result=dirList[maxIndex]
        print(result,"(", maxPr ,")")
    else:
        result="Unknow"
        print(result)  
    end = time.time()    
    fps = round(1 / ( end - start),1)
    cv2.putText(frame, result, (50,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255),2)
    cv2.imshow("Result", frame)    
    key=cv2.waitKey(1)
    # 按q離開
    if key == ord('q'):
        break
# 釋放攝影機
cap.release()
# 關閉所有 OpenCV 視窗
cv2.destroyAllWindows()




