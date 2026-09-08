import numpy as np
import matplotlib

matplotlib.use("Agg")  # SSH/headless 環境：只存圖，不開視窗
import matplotlib.pyplot as plt
from pathlib import Path
from keras.datasets import mnist
from keras.layers import Dense, Flatten, Reshape
from keras.layers import LeakyReLU
from keras.models import Sequential
from keras.optimizers import Adam

img_rows = 28
img_cols = 28
channels = 1  # MNIST圖像皆為灰階
img_shape = (img_rows, img_cols, channels)  # 輸入圖像的尺寸
z_dim = 100  # 指定生成器隨機向量的長度
fixed_sample_noise = np.random.normal(0, 1, (16, z_dim))  # 固定雜訊，方便比較每次迭代進步


def build_generator(img_shape, z_dim):
    model = Sequential()
    model.add(Dense(128, input_dim=z_dim))  # 建立全連接層(隱藏層)
    model.add(LeakyReLU(alpha=0.01))  # 隱藏層激活函數：Leaky ReLU
    model.add(Dense(28 * 28 * 1, activation="tanh"))  # 輸出層激活函數：tanh
    model.add(Reshape(img_shape))  # 重塑輸出圖片的維度
    return model


def build_discriminator(img_shape):
    model = Sequential()
    model.add(Flatten(input_shape=img_shape))  # 將輸入圖像攤平成一維
    model.add(Dense(128))  # 建立全連接層(隱藏層)
    model.add(LeakyReLU(alpha=0.01))  # 激活函數：Leaky ReLU
    model.add(Dense(1, activation="sigmoid"))  # 激活函數：sigmoid
    return model


# 定 義 G A N 函 式
def build_gan(generator, discriminator):
    model = Sequential()
    model.add(generator)
    model.add(discriminator)
    return model


# 建立和編譯鑑別器
discriminator = build_discriminator(img_shape)
discriminator.compile(
    loss="binary_crossentropy", optimizer=Adam(learning_rate=0.0002, beta_1=0.5), metrics=["accuracy"]
)
# 鎖定鑑別器參數以便訓練生成器
discriminator.trainable = False
# 建立生成器
generator = build_generator(img_shape, z_dim)
# 建立和編譯 G A N 模型用以訓練生成器
gan = build_gan(generator, discriminator)
gan.compile(loss="binary_crossentropy", optimizer=Adam(learning_rate=0.0002, beta_1=0.5))

# GAN 編譯時 discriminator 是 frozen；編譯完後要打開，讓 standalone discriminator 可以訓練。
# 如果一直維持 trainable=False，D 不會進步，G 也學不到東西，輸出會一直像雜訊。
discriminator.trainable = True


losses = []
accuracies = []
iteration_checkpoints = []


def train(iterations, batch_size, sample_interval):
    (X_train, _), (_, _) = mnist.load_data()  # 載 入 M N I S T 資料集
    X_train = X_train / 127.5 - 1.0  # 將灰階像素質由 [0, 255] 轉換為 [-1, 1]
    X_train = np.expand_dims(X_train, axis=3)
    real = np.ones((batch_size, 1)) * 0.9  # label smoothing：真圖片標籤設為 0.9，GAN 較穩
    fake = np.zeros((batch_size, 1))  # 將假圖片標籤設為 0
    for iteration in range(iterations):
        # 隨機挑一批真圖片
        idx = np.random.randint(0, X_train.shape[0], batch_size)
        imgs = X_train[idx]
        # 生成一批假圖片
        z = np.random.normal(0, 1, (batch_size, 100))
        gen_imgs = generator(z, training=False).numpy()
        # 訓練鑑別器
        d_loss_real = discriminator.train_on_batch(imgs, real)
        d_loss_fake = discriminator.train_on_batch(gen_imgs, fake)
        d_loss, accuracy = 0.5 * np.add(d_loss_real, d_loss_fake)

        z = np.random.normal(0, 1, (batch_size, 100))
        # 訓練生成器
        g_loss = gan.train_on_batch(z, real)
        if (iteration + 1) % sample_interval == 0:
            # 紀錄損失率及準確率
            losses.append((d_loss, g_loss))
            accuracies.append(100.0 * accuracy)
            iteration_checkpoints.append(iteration + 1)
            # 顯示訓練過程
            print(
                "%d [D loss: %f, acc.: %.2f%%] [G loss: %f]"
                % (iteration + 1, d_loss, 100.0 * accuracy, g_loss)
            )
            # 生成並儲存圖片（SSH 環境不顯示視窗）
            sample_images(generator, iteration + 1)


def sample_images(generator, iteration, image_grid_rows=4, image_grid_columns=4):
    z = fixed_sample_noise[: image_grid_rows * image_grid_columns] # 使用固定雜訊，才看得出同一組輸入的演化
    gen_imgs = generator(z, training=False).numpy() # 用這組隨機雜訊生成圖片
    gen_imgs = 0.5 * gen_imgs + 0.5 # 將圖片像素質由 [-1, 1] 轉換為 [0, 1]
    fig, axs = plt.subplots(image_grid_rows, image_grid_columns, figsize=(4, 4),
    sharey=True, sharex=True) # 設定圖片網格
    cnt = 0
    for i in range(image_grid_rows):
        for j in range(image_grid_columns):
            axs[i, j].imshow(gen_imgs[cnt, :, :, 0], cmap="gray")
            axs[i, j].axis("off")
            cnt += 1

    output_dir = Path("generated_images")
    output_dir.mkdir(exist_ok=True)
    output_path = output_dir / f"mnist_{iteration:06d}.png"
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close(fig)
    print(f"Saved image: {output_path}")

# 設定超參數
iterations = 20000
batch_size = 128
sample_interval = 1000
train(iterations, batch_size, sample_interval)
