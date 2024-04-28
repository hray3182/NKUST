from tensorflow import keras
from keras.datasets import cifar10


(x_train, y_train), (x_test, y_test) = cifar10.load_data()

# Normalize the data - 正規化
x_train = x_train / 255
x_test = x_test / 255

from keras.utils import to_categorical

# 類別化 -> 3 -> [0, 0, 0, 1, 0, 0, 0, 0, 0, 0] 機率矩陣
y_train = to_categorical(y_train)
y_test = to_categorical(y_test)

# 建立模型 
from keras.models import Sequential
model = Sequential()


# 建立 CNN 網路
from keras.layers import Conv2D, Dense, Dropout, Flatten, MaxPool2D
model.add(
    Conv2D(
        input_shape = (32, 32, 3), # 輸入不可變更
        filters=64, # 卷積核 # 邊緣濾鏡、垂直濾鏡等
        kernel_size=(3,3), # 卷積核大小
        activation='relu'
    )
)

# 最大池化層
model.add(
    MaxPool2D(
        pool_size = (2, 2) # 縮一半
    )
)

# 做完一次卷積 + 池化後資料量會變成 15 * 15 * 3


# 再多做一次卷積 + 池化
model.add(
    Conv2D(
        filters = 1024,
        kernel_size = (3, 3),
        activation = 'relu'
    )
)

model.add(
    MaxPool2D(
        pool_size = (2, 2)
    )
)

# 卷積 + 池化會降低圖片解析度


# 將資料拉成一維
model.add(Flatten())


# 傳統神經網路
model.add(Dropout(rate = 0.2)) # 遺忘 20%
model.add(Dense(units = 128, activation = 'relu'))
model.add(Dropout(rate = 0.2))
model.add(Dense(units = 10, activation = 'softmax')) # 輸出層 


# 編譯模型
model.compile(
    optimizer = 'adam', # 最佳化函數
    loss = 'categorical_crossentropy', # 損失評估=類別交叉熵
    metrics = ['accuracy'] # 評估方式=正確率
)

model.summary()


# 開始訓練
train_history = model.fit(x=x_train, y=y_train , validation_split=0.2, epochs=10, batch_size=32, verbose=1)  

#評估
loss, accuracy = model.evaluate(x_test, y_test)
print('test loss: ', loss)
print('test accuracy: ', accuracy)

#畫出訓練過程圖
import matplotlib.pyplot as plt
def show_train_history(train_history, train, validation):
    plt.plot(train_history.history[train])  
    plt.plot(train_history.history[validation])  
    plt.title('Train History')  
    plt.ylabel(train)  
    plt.xlabel('Epoch')  
    plt.legend(['train', 'test'], loc='upper left')  
    plt.show()
show_train_history(train_history, 'accuracy', 'val_accuracy')  


#
model.save('week10\cifar10.keras')