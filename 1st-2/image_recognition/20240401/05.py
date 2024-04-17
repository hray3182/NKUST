import matplotlib.pyplot as plt
import tensorflow as tf
#import pandas as pd #pip install pandas
mnist = tf.keras.datasets.mnist
from tensorflow.keras.utils import to_categorical

print(tf.config.list_physical_devices('GPU'))

#1.準備資料
(x_train, y_train), (x_test, y_test) = mnist.load_data()
x_train=x_train.reshape((60000, 28, 28, 1))/255.0
x_test=x_test.reshape((10000, 28, 28, 1))/255.0
y_train = to_categorical(y_train, num_classes=10) #[3]->[0,0,0,1,0,0,0,0,0,0,0]
y_test = to_categorical(y_test, num_classes=10)


def plot_image(image):  
    fig = plt.gcf()  
    fig.set_size_inches(2,2)  
    plt.imshow(image, cmap='binary') # cmap='binary' 參數設定以黑白灰階顯示.  
    plt.show()
plot_image(x_train[0])
#2.建立Sequential模型

model = tf.keras.models.Sequential()
#每次卷積後，圖形大小會減少卷積-1，每次池化大小會/2
#16個3x3卷積核                   數量:8的倍數   大小:3,5,7奇數                長28x寬28x顏色1
model.add(tf.keras.layers.Conv2D(16, (3, 3), activation='relu', input_shape=(28, 28, 1)))
model.add(tf.keras.layers.MaxPooling2D((2, 2)))
#model.add(tf.keras.layers.Dropout(0.2))
#32個5x5卷積核
model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu'))
model.add(tf.keras.layers.MaxPooling2D((2, 2)))
#model.add(tf.keras.layers.Dropout(0.2))
#轉平面層
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dropout(0.2))
model.add(tf.keras.layers.Dense(32, activation='relu'))
model.add(tf.keras.layers.Dropout(0.2))
model.add(tf.keras.layers.Dense(10, activation='softmax'))
model.summary() # 显示模型的架构
model.compile(optimizer='adam', #tf.keras.optimizers.Adam(learning_rate=0.01),
              loss='categorical_crossentropy',
              metrics=['accuracy'])
                                          #48000/200=2400,  2400*50=120000
train_history =model.fit(x_train, y_train,batch_size=200, epochs=20,validation_split=0.2, verbose=1)
#顯示訓練過程
def show_train_history(train_history, train, validation):  
    plt.plot(train_history.history[train])  
    plt.plot(train_history.history[validation])  
    plt.title('Train History')  
    plt.ylabel(train)  
    plt.xlabel('Epoch')  
    plt.legend(['train', 'validation'], loc='upper left')  
    plt.show()
show_train_history(train_history, 'accuracy', 'val_accuracy')  

#4.評估模型
loss, accuracy = model.evaluate(x_test, y_test)
print('test loss: ', loss)
print('test accuracy: ', accuracy)
#print(pd.crosstab(y_test, prediction,rownames=['實際'], colnames=['預測']))


#5.儲存模型檔案
model.save('CNNMnist.keras')