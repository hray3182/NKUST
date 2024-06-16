import tensorflow as tf
import pandas as pd
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Dropout
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.regularizers import l2
import tensorflow_addons as tfa

# 讀取標籤
train_annotations = pd.read_csv('cars_train_annos.mat.csv')
test_annotations = pd.read_csv('cars_test_annos.mat.csv')
brands = pd.read_csv('brand.csv')

# 建立品牌字典
brand_dict = {row['brand']: row['brand_id'] for _, row in brands.iterrows()}

# 添加品牌 ID 到訓練和測試數據
train_annotations['brand_id'] = train_annotations['brand'].map(brand_dict)
test_annotations['brand_id'] = test_annotations['brand'].map(brand_dict)

# 確保標籤是字符串類型
train_annotations['brand_id'] = train_annotations['brand_id'].astype(str)
test_annotations['brand_id'] = test_annotations['brand_id'].astype(str)

# 數據增強和預處理
train_datagen = ImageDataGenerator(
    rescale=1./255,
    shear_range=0.2,
    zoom_range=0.2,
    rotation_range=20,
    brightness_range=(0.8, 1.2),
    horizontal_flip=True,
    fill_mode='nearest'
)

test_datagen = ImageDataGenerator(rescale=1./255)

# 生成訓練數據
train_generator = train_datagen.flow_from_dataframe(
    dataframe=train_annotations,
    directory='archive/cars_train',
    x_col='image',
    y_col='brand_id',
    target_size=(224, 224),
    batch_size=32,
    class_mode='sparse'
)

# 生成測試數據
test_generator = test_datagen.flow_from_dataframe(
    dataframe=test_annotations,
    directory='archive/cars_test',
    x_col='image',
    y_col='brand_id',
    target_size=(224, 224),
    batch_size=32,
    class_mode='sparse',
    shuffle=False
)

# 使用 ResNet50 預訓練模型
base_model = ResNet50(weights='imagenet', include_top=False)

# 池化層
x = base_model.output
x = GlobalAveragePooling2D()(x)

# 全連接層
x = Dense(1024, activation='relu', kernel_regularizer=l2(0.005))(x)
x = Dropout(0.5)(x)
x = Dense(512, activation='relu', kernel_regularizer=l2(0.005))(x)
x = Dropout(0.5)(x)

# 輸出層
predictions = Dense(len(brand_dict), activation='softmax')(x)

# 定義模型
model = Model(inputs=base_model.input, outputs=predictions)

# 凍結前 30 層
for layer in base_model.layers[-50:]:
    layer.trainable = True

# 編譯模型
optimizer = tfa.optimizers.AdamW(learning_rate=0.0001, weight_decay=0.0001)
model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

# 定義 callbacks
early_stopping = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True, mode='min')
reduce_lr = ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=0.000001)
checkpoint = ModelCheckpoint('best_model.h5', monitor='val_accuracy', save_best_only=True, mode='max')

# 訓練模型
# model.fit(
#     train_generator,
#     steps_per_epoch=train_generator.n // train_generator.batch_size,
#     epochs=50,
#     validation_data=test_generator,
#     validation_steps=test_generator.n // test_generator.batch_size,
#     validation_freq=1,
#     callbacks=[early_stopping, reduce_lr, checkpoint]
# )

# save model
# model.save('car_brand_model_final.h5')

model = tf.keras.models.load_model('best_model.h5')

# evaluate model
loss, accuracy = model.evaluate(test_generator, steps=test_generator.n // test_generator.batch_size)
print(f'Test loss: {loss}')
print(f'Test accuracy: {accuracy}')
