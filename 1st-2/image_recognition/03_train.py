import tensorflow as tf
print('tf版本=',tf.__version__)
import matplotlib.pyplot as plt
size=(200,200)
batchSize=32
trainFileCount=320 #訓練檔案數量
testFileCount=80 #測試檔案數量
# 簡單的三層卷積加上ReLU啟用函式，再接一個max-pooling層
model = tf.keras.models.Sequential()
#32個3x3卷積核
model.add(tf.keras.layers.Conv2D(32, (3, 3), activation='relu', input_shape=(200, 200, 3)))
model.add(tf.keras.layers.MaxPooling2D((2, 2)))
#64個3x3卷積核
model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
model.add(tf.keras.layers.MaxPooling2D((2, 2)))

#model.add(tf.keras.layers.Conv2D(64, (3, 3), activation='relu'))
#model.add(tf.keras.layers.MaxPooling2D((2, 2)))

#轉平面層
model.add(tf.keras.layers.Flatten())
model.add(tf.keras.layers.Dense(128, activation='relu'))
model.add(tf.keras.layers.Dropout(0.2))
model.add(tf.keras.layers.Dense(64, activation='relu'))
model.add(tf.keras.layers.Dropout(0.2))
model.add(tf.keras.layers.Dense(4, activation='softmax'))
model.compile(optimizer= "adam",#tf.keras.optimizers.Adam(learning_rate=0.001),
              loss='categorical_crossentropy',
              metrics=['accuracy'])
model.summary() # 顯示類神經架構

#訓練的圖片生成器
train_ImgDataGen = tf.keras.preprocessing.image.ImageDataGenerator(  
    rotation_range=20,#隨機旋轉 +-20度
    width_shift_range=0.2,#x軸平移 +-20%
    height_shift_range=0.2,#y軸平移 +-20%
    shear_range=0.2, #平行錯位 +-20%
    zoom_range=0.2,#放大縮小 +-20%
    #channel_shift_range=0., #隨機顏色濾鏡
    fill_mode='nearest',#填入模式    
    #horizontal_flip=True,#水平翻轉
    #vertical_flip=True,#垂直翻轉
    rescale=1.0/255,#重新配置範圍0~255 -> 0~1
    )

#指定訓練圖片路徑參數
train_generator = train_ImgDataGen.flow_from_directory(
    'train',#訓練樣本路徑
    target_size=size,
    batch_size=batchSize,
    class_mode='categorical' #多分類
    )

#驗證的圖片生成器
test_ImgDataGen = tf.keras.preprocessing.image.ImageDataGenerator(
    rescale= 1.0 /255,
    )

#指定驗證圖片路徑參數
validation_generator = test_ImgDataGen.flow_from_directory(
    'test',#驗證樣本路徑
    target_size=size,
    batch_size=batchSize,
    class_mode='categorical', #多分類
    )
 
# 然後我們可以用這個生成器來訓練網路了。
train_history=model.fit_generator(    
    train_generator, #指定訓練圖片生成器
    steps_per_epoch = trainFileCount//batchSize, #一個世代幾批次=訓練檔案總量/批次量
    epochs=3,
    verbose=1,
    validation_steps =testFileCount//batchSize ,#一個世代幾批次=測試檔案總量/批次量
    validation_data=validation_generator, #指定驗證圖片生成器
    #callbacks=callbacks_list,#紀錄點
    )

model.save('CNN_RPS.keras')

def show_train_history(train_history, train, validation):  
    plt.plot(train_history.history[train])  
    plt.plot(train_history.history[validation])  
    plt.title('Train History')  
    plt.ylabel(train)  
    plt.xlabel('Epoch')  
    plt.legend(['train', 'validation'], loc='upper left')  
    plt.show()

show_train_history(train_history, 'accuracy', 'val_accuracy')  

