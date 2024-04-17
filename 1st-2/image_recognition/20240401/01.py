import tensorflow as tf
import keras as ks
print(tf.__version__)
print(ks.__version__)
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.datasets import mnist
from tensorflow.keras.utils import to_categorical


(X_train, Y_train), (X_test, Y_test_S) = mnist.load_data()


def plot_image(image):  
    fig = plt.gcf()  
    fig.set_size_inches(2,2)  
    plt.imshow(image, cmap='binary') # cmap='binary'  
    plt.show()
plot_image(X_train[0])

X_train = X_train.reshape(X_train.shape[0], -1)/255 #
X_test = X_test.reshape(X_test.shape[0], -1)/255 #
Y_train = to_categorical(Y_train, num_classes=10) #[3]->[0,0,0,1,0,0,0,0,0,0,0]
Y_test = to_categorical(Y_test_S, num_classes=10)

#
model = Sequential()
model.add(Dense(128, input_dim=784))
model.add(Activation('relu')) #relu
model.add(Dense(10))
model.add(Activation('softmax')) 
model.compile(optimizer='adam',loss='categorical_crossentropy',metrics=['accuracy']) 
model.summary()
#3.
train_history = model.fit(x=X_train, y=Y_train , validation_split=0.2, epochs=10, batch_size=200, verbose=2)  


#4
loss, accuracy = model.evaluate(X_test, Y_test)
print('test loss: ', loss)
print('test accuracy: ', accuracy)


#
def show_train_history(train_history, train, validation): 
    plt.plot(train_history.history[train])  
    plt.plot(train_history.history[validation])  
    plt.title('Train History')  
    plt.ylabel(train)  
    plt.xlabel('Epoch')  
    plt.legend(['train', 'test'], loc='upper left')  
    plt.show()
show_train_history(train_history, 'accuracy', 'val_accuracy')  


#5.
model.save('mnist.keras')


