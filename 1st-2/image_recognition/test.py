# print tf version

import tensorflow as tf
print(tf.__version__)

# list gpu
from tensorflow.python.client import device_lib
physical_devices = tf.config.list_physical_devices('GPU')
print(physical_devices)