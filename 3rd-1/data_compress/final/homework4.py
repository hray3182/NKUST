import numpy as np
from sklearn.cluster import KMeans


class VectorQuantizer:
    def __init__(self, n_codewords=8, block_size=2):
        self.n_codewords = n_codewords
        self.block_size = block_size
        self.codebook = None
        self.kmeans = None

    def split_into_blocks(self, matrix):
        h, w = matrix.shape
        blocks = []

        for i in range(0, h, self.block_size):
            for j in range(0, w, self.block_size):
                block = matrix[i : i + self.block_size, j : j + self.block_size]
                if block.shape == (self.block_size, self.block_size):
                    blocks.append(block.flatten())

        return np.array(blocks)

    def train(self, training_data):
        all_blocks = []

        if isinstance(training_data, np.ndarray) and training_data.ndim == 2:
            training_data = [training_data]

        for matrix in training_data:
            blocks = self.split_into_blocks(matrix)
            all_blocks.extend(blocks)

        all_blocks = np.array(all_blocks)

        self.kmeans = KMeans(n_clusters=self.n_codewords, random_state=42, n_init=10)
        self.kmeans.fit(all_blocks)
        self.codebook = self.kmeans.cluster_centers_

        return self.codebook

    def encode(self, matrix):
        blocks = self.split_into_blocks(matrix)
        indices = self.kmeans.predict(blocks)
        return indices

    def decode(self, indices, original_shape):
        h, w = original_shape
        reconstructed = np.zeros((h, w))

        idx = 0
        for i in range(0, h, self.block_size):
            for j in range(0, w, self.block_size):
                if idx < len(indices):
                    block = self.codebook[indices[idx]].reshape(
                        self.block_size, self.block_size
                    )
                    reconstructed[i : i + self.block_size, j : j + self.block_size] = (
                        block
                    )
                    idx += 1

        return reconstructed


def main():
    test_matrix = np.array(
        [
            [139, 144, 149, 153, 155, 155, 155, 155],
            [144, 151, 153, 156, 159, 156, 156, 156],
            [150, 155, 160, 163, 158, 156, 156, 156],
            [159, 161, 162, 160, 160, 159, 159, 159],
            [159, 160, 161, 162, 162, 155, 155, 155],
            [161, 161, 161, 161, 160, 157, 157, 157],
            [162, 162, 161, 163, 162, 157, 157, 157],
            [162, 162, 161, 161, 163, 158, 158, 158],
        ],
        dtype=float,
    )

    print("Input (8x8 matrix):")
    print(test_matrix.astype(int))
    print()

    # 向量量化：K=8, block_size=2x2
    vq = VectorQuantizer(n_codewords=8, block_size=2)
    vq.train(test_matrix)

    print("Output - Codebook (K=8):")
    for i, codeword in enumerate(vq.codebook):
        print(f"Codeword {i}:")
        print(codeword.reshape(2, 2).round(2))
        print()


if __name__ == "__main__":
    main()
