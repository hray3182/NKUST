from tensorflow import keras
from keras.datasets import cifar10

(x_train, y_train), (x_test, y_test) = cifar10.load_data()
print(x_train.shape)

import matplotlib.pyplot as plt
from random import randrange

plt.figure(figsize=(16,10), facecolor="w")
for i in range(5):
    for j in range(8):
        index = randrange(len(x_train))
        plt.subplot(5, 8, i*8+j+1)
        plt.title("label: %d" % y_train[index])
        plt.imshow(x_train[index])
        plt.axis("off")

plt.show()