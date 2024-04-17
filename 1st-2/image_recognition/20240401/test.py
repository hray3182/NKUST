import tensorflow as tf
print(tf.config.list_physical_devices('GPU'))


# 檢查 TensorFlow 版本
print(tf.__version__)

# 檢查 TensorFlow 是否可以存取 GPU
if tf.test.is_gpu_available():
    print("GPU is available")
else:
    print("GPU is not available")