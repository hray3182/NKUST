"""
K-means Image Compression
把 input 資料夾的圖片壓縮後放到 output 資料夾
"""

import numpy as np
from sklearn.cluster import KMeans
from PIL import Image
import os

# 設定
INPUT_DIR = "input"
OUTPUT_DIR = "output"
K = 32  # 聚類數量（顏色數）


def compress_image(image_path, k):
    """使用 K-means 壓縮圖片"""
    # 讀取圖片
    img = Image.open(image_path).convert("RGB")
    original = np.array(img)
    h, w, c = original.shape

    # 把圖片轉成像素列表 (H*W, 3)
    pixels = original.reshape(-1, 3).astype(np.float64)

    # K-means 聚類
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(pixels)
    centroids = kmeans.cluster_centers_

    # 用聚類中心重建圖片
    compressed_pixels = centroids[labels]
    compressed = compressed_pixels.reshape(h, w, c).astype(np.uint8)

    return original, compressed, centroids


def calculate_metrics(original, compressed, k):
    """計算壓縮率和失真率"""
    h, w, c = original.shape

    # 壓縮率計算
    # 原始: H * W * 3 * 8 bits
    # 壓縮: codebook (K * 3 * 8 bits) + indices (H * W * log2(K) bits)
    original_bits = h * w * c * 8
    codebook_bits = k * 3 * 8
    indices_bits = h * w * np.ceil(np.log2(k))
    compressed_bits = codebook_bits + indices_bits
    compression_ratio = original_bits / compressed_bits

    # MSE (Mean Squared Error)
    mse = np.mean((original.astype(np.float64) - compressed.astype(np.float64)) ** 2)

    # PSNR (Peak Signal-to-Noise Ratio)
    if mse == 0:
        psnr = float("inf")
    else:
        psnr = 10 * np.log10((255**2) / mse)

    return compression_ratio, mse, psnr


def main():
    # 建立資料夾
    os.makedirs(INPUT_DIR, exist_ok=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # 取得 input 資料夾中的圖片
    image_extensions = (".bmp", ".tif", ".tiff")
    images = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(image_extensions)]

    if not images:
        print(f"[INFO] input 資料夾是空的，請放入圖片")
        print(f"[INFO] 支援的格式: {image_extensions}")
        return

    print(f"[INFO] 找到 {len(images)} 張圖片")
    print(f"[INFO] K = {K} (顏色數)")
    print("=" * 60)

    for filename in images:
        input_path = os.path.join(INPUT_DIR, filename)
        output_filename = os.path.splitext(filename)[0] + f"_k{K}.png"
        output_path = os.path.join(OUTPUT_DIR, output_filename)

        print(f"\n[處理中] {filename}")

        # 壓縮圖片
        original, compressed, centroids = compress_image(input_path, K)

        # 計算指標
        compression_ratio, mse, psnr = calculate_metrics(original, compressed, K)

        # 儲存壓縮後的圖片
        Image.fromarray(compressed).save(output_path)

        # 輸出結果
        h, w, c = original.shape
        print(f"  圖片尺寸: {w} x {h}")
        print(f"  壓縮率: {compression_ratio:.2f}:1")
        print(f"  MSE (均方誤差): {mse:.2f}")
        print(f"  PSNR (峰值信噪比): {psnr:.2f} dB")
        print(f"  輸出: {output_path}")

    print("\n" + "=" * 60)
    print("[完成] 所有圖片已壓縮完成")


if __name__ == "__main__":
    main()
