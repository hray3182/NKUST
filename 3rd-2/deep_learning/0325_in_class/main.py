from keras.datasets import boston_housing

(train_data, train_targets), (test_data, test_targets) = boston_housing.load_data()


mean = train_data.mean(axis=0)  # 沿著第 0 軸 (batch_size 軸) 做平均
train_data -= mean
std = train_data.std(axis=0)  # 沿著第 0 軸 (batch_size 軸) 算標準差
train_data /= std
test_data -= mean
test_data /= std

from keras import models
from keras import layers


def build_model():
    model = models.Sequential()  # 建構一個 sequential 模型
    model.add(layers.Dense(64, activation="relu", input_shape=(train_data.shape[1],)))
    model.add(layers.Dense(64, activation="relu"))
    model.add(layers.Dense(1))
    model.compile(optimizer="rmsprop", loss="mse", metrics=["mae"])
    return model


import numpy as np

k = 4  # 進行 4 折交叉驗證
num_val_samples = len(train_data) // k  # 驗證區塊的樣本數
num_epochs = 100
all_scores = []
for i in range(k):
    print("processing fold #", i)  # 準備驗證資料：資料來自 #k 區塊
    val_data = train_data[i * num_val_samples : (i + 1) * num_val_samples]
    val_targets = train_targets[i * num_val_samples : (i + 1) * num_val_samples]
    partial_train_data = np.concatenate(  # 準備訓練資料：資料來自 #k 以外的所有區塊
        [train_data[: i * num_val_samples], train_data[(i + 1) * num_val_samples :]],
        axis=0,
    )
    partial_train_targets = np.concatenate(
        [
            train_targets[: i * num_val_samples],
            train_targets[(i + 1) * num_val_samples :],
        ],
        axis=0,
    )


model = build_model()  # 建構 Keras 模型(已編譯)
model.fit(
    partial_train_data,
    partial_train_targets,
    epochs=num_epochs,
    batch_size=1,
    verbose=0,
)  # 訓練該模型
val_mse, val_mae = model.evaluate(
    val_data, val_targets, verbose=0
)  # 以驗證資料來評估模型
all_scores.append(val_mae)


print(all_scores)

print(np.mean(all_scores))
