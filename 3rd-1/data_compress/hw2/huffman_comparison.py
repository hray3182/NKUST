import numpy as np
from PIL import Image
from collections import Counter, defaultdict
import heapq
from typing import Dict, Tuple

class Node:
    def __init__(self, symbol=None, freq=0, left=None, right=None):
        self.symbol = symbol
        self.freq = freq
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(frequency_dict: Dict) -> Node:
    """Build Huffman tree from frequency dictionary"""
    heap = [Node(symbol=symbol, freq=freq) for symbol, freq in frequency_dict.items()]
    heapq.heapify(heap)

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        parent = Node(freq=left.freq + right.freq, left=left, right=right)
        heapq.heappush(heap, parent)

    return heap[0] if heap else None

def generate_codes(root: Node, code: str = "", codes: Dict = None) -> Dict:
    """Generate Huffman codes from tree"""
    if codes is None:
        codes = {}

    if root is None:
        return codes

    if root.symbol is not None:
        codes[root.symbol] = code if code else "0"
        return codes

    generate_codes(root.left, code + "0", codes)
    generate_codes(root.right, code + "1", codes)

    return codes

def calculate_compression_stats(data, codes: Dict) -> Tuple[float, float, float]:
    """Calculate compression statistics"""
    # Original size in bits (assuming 8 bits per value)
    original_bits = len(data) * 8

    # Compressed size in bits
    compressed_bits = sum(len(codes[value]) for value in data)

    # Average code length
    avg_code_length = compressed_bits / len(data)

    # Compression ratio
    compression_ratio = original_bits / compressed_bits

    return original_bits, compressed_bits, avg_code_length, compression_ratio

def method_a_basic_huffman(image_array: np.ndarray) -> Dict:
    """Method A: Basic Huffman coding on pixel values"""
    print("=" * 60)
    print("METHOD A: Basic Huffman Coding")
    print("=" * 60)

    # Flatten the image to 1D array
    flat_data = image_array.flatten()

    # Calculate frequency
    frequency = Counter(flat_data)
    print(f"Number of unique pixel values: {len(frequency)}")
    print(f"Total pixels: {len(flat_data)}")

    # Build Huffman tree and generate codes
    tree = build_huffman_tree(frequency)
    codes = generate_codes(tree)

    # Calculate statistics
    original_bits, compressed_bits, avg_code_length, compression_ratio = \
        calculate_compression_stats(flat_data, codes)

    print(f"\nResults:")
    print(f"  Original size: {original_bits:,} bits ({original_bits / 8:,.0f} bytes)")
    print(f"  Compressed size: {compressed_bits:,} bits ({compressed_bits / 8:,.2f} bytes)")
    print(f"  Average code length: {avg_code_length:.4f} bits")
    print(f"  Compression ratio: {compression_ratio:.4f}:1")
    print(f"  Space savings: {(1 - compressed_bits/original_bits) * 100:.2f}%")

    # Show some example codes
    print(f"\nSample Huffman codes (first 10):")
    for i, (value, code) in enumerate(list(codes.items())[:10]):
        print(f"  Pixel value {value}: {code} (length: {len(code)})")

    return {
        'codes': codes,
        'frequency': frequency,
        'original_bits': original_bits,
        'compressed_bits': compressed_bits,
        'avg_code_length': avg_code_length,
        'compression_ratio': compression_ratio
    }

def method_b_differential_huffman(image_array: np.ndarray) -> Dict:
    """Method B: Huffman coding on pixel differences"""
    print("\n" + "=" * 60)
    print("METHOD B: Huffman Coding on Pixel Differences")
    print("=" * 60)

    # Calculate differences between adjacent pixels
    # We'll use horizontal differences (current pixel - previous pixel)
    differences = []

    height, width = image_array.shape[:2]

    if len(image_array.shape) == 3:
        # Color image - process each channel
        for channel in range(image_array.shape[2]):
            for row in range(height):
                for col in range(width):
                    if col == 0:
                        # First pixel in row - use pixel value itself
                        diff = image_array[row, col, channel]
                    else:
                        # Difference from previous pixel
                        diff = int(image_array[row, col, channel]) - int(image_array[row, col-1, channel])
                    differences.append(diff)
    else:
        # Grayscale image
        for row in range(height):
            for col in range(width):
                if col == 0:
                    diff = image_array[row, col]
                else:
                    diff = int(image_array[row, col]) - int(image_array[row, col-1])
                differences.append(diff)

    # Calculate frequency
    frequency = Counter(differences)
    print(f"Number of unique difference values: {len(frequency)}")
    print(f"Total differences: {len(differences)}")
    print(f"Difference range: [{min(differences)}, {max(differences)}]")

    # Build Huffman tree and generate codes
    tree = build_huffman_tree(frequency)
    codes = generate_codes(tree)

    # Calculate statistics
    original_bits, compressed_bits, avg_code_length, compression_ratio = \
        calculate_compression_stats(differences, codes)

    print(f"\nResults:")
    print(f"  Original size: {original_bits:,} bits ({original_bits / 8:,.0f} bytes)")
    print(f"  Compressed size: {compressed_bits:,} bits ({compressed_bits / 8:,.2f} bytes)")
    print(f"  Average code length: {avg_code_length:.4f} bits")
    print(f"  Compression ratio: {compression_ratio:.4f}:1")
    print(f"  Space savings: {(1 - compressed_bits/original_bits) * 100:.2f}%")

    # Show distribution of differences
    print(f"\nDifference distribution (top 10 most frequent):")
    for diff, count in frequency.most_common(10):
        percentage = (count / len(differences)) * 100
        print(f"  Difference {diff:4d}: {count:6d} occurrences ({percentage:5.2f}%), code: {codes[diff]}")

    return {
        'codes': codes,
        'frequency': frequency,
        'differences': differences,
        'original_bits': original_bits,
        'compressed_bits': compressed_bits,
        'avg_code_length': avg_code_length,
        'compression_ratio': compression_ratio
    }

def compare_results(result_a: Dict, result_b: Dict):
    """Compare the results of both methods"""
    print("\n" + "=" * 60)
    print("COMPARISON AND ANALYSIS")
    print("=" * 60)

    print(f"\nCompression Ratio:")
    print(f"  Method A (Basic):       {result_a['compression_ratio']:.4f}:1")
    print(f"  Method B (Differential): {result_b['compression_ratio']:.4f}:1")

    if result_b['compression_ratio'] > result_a['compression_ratio']:
        improvement = ((result_b['compression_ratio'] / result_a['compression_ratio']) - 1) * 100
        print(f"  Method B is {improvement:.2f}% better")
    else:
        degradation = ((result_a['compression_ratio'] / result_b['compression_ratio']) - 1) * 100
        print(f"  Method A is {degradation:.2f}% better")

    print(f"\nAverage Code Length:")
    print(f"  Method A (Basic):       {result_a['avg_code_length']:.4f} bits")
    print(f"  Method B (Differential): {result_b['avg_code_length']:.4f} bits")

    print(f"\nCompressed Size:")
    print(f"  Method A (Basic):       {result_a['compressed_bits']:,} bits ({result_a['compressed_bits']/8:,.2f} bytes)")
    print(f"  Method B (Differential): {result_b['compressed_bits']:,} bits ({result_b['compressed_bits']/8:,.2f} bytes)")

    space_diff = result_a['compressed_bits'] - result_b['compressed_bits']
    print(f"  Difference: {abs(space_diff):,} bits ({abs(space_diff)/8:,.2f} bytes)")

    print(f"\nSymbol Diversity:")
    print(f"  Method A: {len(result_a['frequency'])} unique symbols")
    print(f"  Method B: {len(result_b['frequency'])} unique symbols")

    print(f"\n" + "-" * 60)
    print("ANALYSIS:")
    print("-" * 60)

    print("""
Method A (Basic Huffman):
  - Encodes each pixel value directly
  - Works well when pixel values have non-uniform distribution
  - No exploitation of spatial correlation between pixels

Method B (Differential Huffman):
  - Encodes the differences between adjacent pixels
  - Exploits spatial correlation in images
  - Small differences are more frequent (pixels tend to be similar to neighbors)
  - This creates a more peaked distribution, leading to better compression

Key Observations:
  - Adjacent pixels in natural images are highly correlated
  - Differences between adjacent pixels cluster around 0
  - This creates a more skewed probability distribution
  - Huffman coding benefits from skewed distributions
  - Method B typically achieves better compression for natural images
    """)

def main():
    # Load the image
    image_path = "1067.jpg"
    print(f"Loading image: {image_path}")

    img = Image.open(image_path)
    print(f"Image size: {img.size} (width x height)")
    print(f"Image mode: {img.mode}")

    # Convert to numpy array
    img_array = np.array(img)
    print(f"Array shape: {img_array.shape}")

    # Method A: Basic Huffman coding
    result_a = method_a_basic_huffman(img_array)

    # Method B: Differential Huffman coding
    result_b = method_b_differential_huffman(img_array)

    # Compare results
    compare_results(result_a, result_b)

if __name__ == "__main__":
    main()
