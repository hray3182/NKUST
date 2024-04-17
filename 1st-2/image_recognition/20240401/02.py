
import cv2
import keras
import numpy as np
model=keras.models.load_model('mnist.h5')
img = cv2.imread('test1.jpg')
img = cv2.resize(img,(28,28))
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
pixel=[]
for i in range(28):
    for j in range(28):
        pixel.append((255-gray[i,j])/255)
pixelarray=np.asarray([pixel])
label=model.predict(pixelarray)
maxindex = np.argmax(label)
if label.max()>0.8:
    print(maxindex)
else:
    print('無法確認')