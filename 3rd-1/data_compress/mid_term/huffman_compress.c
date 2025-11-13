#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_TREE_HT 256

// Huffman tree node structure
typedef struct MinHeapNode {
    char data;                      // Character
    unsigned freq;                  // Frequency of the character
    struct MinHeapNode *left, *right;  // Left and right child nodes
} MinHeapNode;

// Min heap structure for building Huffman tree
typedef struct MinHeap {
    unsigned size;                  // Current size of the heap
    unsigned capacity;              // Maximum capacity
    MinHeapNode** array;            // Array of node pointers
} MinHeap;

// Create a new min heap node
MinHeapNode* newNode(char data, unsigned freq) {
    MinHeapNode* temp = (MinHeapNode*)malloc(sizeof(MinHeapNode));
    temp->left = temp->right = NULL;
    temp->data = data;
    temp->freq = freq;
    return temp;
}

// Create a min heap with given capacity
MinHeap* createMinHeap(unsigned capacity) {
    MinHeap* minHeap = (MinHeap*)malloc(sizeof(MinHeap));
    minHeap->size = 0;
    minHeap->capacity = capacity;
    minHeap->array = (MinHeapNode**)malloc(minHeap->capacity * sizeof(MinHeapNode*));
    return minHeap;
}

// Swap two min heap nodes
void swapMinHeapNode(MinHeapNode** a, MinHeapNode** b) {
    MinHeapNode* t = *a;
    *a = *b;
    *b = t;
}

// Heapify the min heap at given index
void minHeapify(MinHeap* minHeap, int idx) {
    int smallest = idx;
    int left = 2 * idx + 1;
    int right = 2 * idx + 2;

    if (left < minHeap->size && minHeap->array[left]->freq < minHeap->array[smallest]->freq)
        smallest = left;

    if (right < minHeap->size && minHeap->array[right]->freq < minHeap->array[smallest]->freq)
        smallest = right;

    if (smallest != idx) {
        swapMinHeapNode(&minHeap->array[smallest], &minHeap->array[idx]);
        minHeapify(minHeap, smallest);
    }
}

// Check if heap size is one
int isSizeOne(MinHeap* minHeap) {
    return (minHeap->size == 1);
}

// Extract minimum value node from heap
MinHeapNode* extractMin(MinHeap* minHeap) {
    MinHeapNode* temp = minHeap->array[0];
    minHeap->array[0] = minHeap->array[minHeap->size - 1];
    --minHeap->size;
    minHeapify(minHeap, 0);
    return temp;
}

// Insert a new node into min heap
void insertMinHeap(MinHeap* minHeap, MinHeapNode* minHeapNode) {
    ++minHeap->size;
    int i = minHeap->size - 1;

    while (i && minHeapNode->freq < minHeap->array[(i - 1) / 2]->freq) {
        minHeap->array[i] = minHeap->array[(i - 1) / 2];
        i = (i - 1) / 2;
    }
    minHeap->array[i] = minHeapNode;
}

// Build the min heap
void buildMinHeap(MinHeap* minHeap) {
    int n = minHeap->size - 1;
    for (int i = (n - 1) / 2; i >= 0; --i)
        minHeapify(minHeap, i);
}

// Check if node is a leaf node
int isLeaf(MinHeapNode* root) {
    return !(root->left) && !(root->right);
}

// Create and build min heap from character frequencies
MinHeap* createAndBuildMinHeap(char data[], int freq[], int size) {
    MinHeap* minHeap = createMinHeap(size);
    for (int i = 0; i < size; ++i)
        minHeap->array[i] = newNode(data[i], freq[i]);
    minHeap->size = size;
    buildMinHeap(minHeap);
    return minHeap;
}

// Build Huffman tree from character data and frequencies
MinHeapNode* buildHuffmanTree(char data[], int freq[], int size) {
    MinHeapNode *left, *right, *top;
    MinHeap* minHeap = createAndBuildMinHeap(data, freq, size);

    // Build tree by combining two minimum frequency nodes
    while (!isSizeOne(minHeap)) {
        left = extractMin(minHeap);
        right = extractMin(minHeap);

        // Create internal node with sum of frequencies
        top = newNode('$', left->freq + right->freq);
        top->left = left;
        top->right = right;

        insertMinHeap(minHeap, top);
    }

    return extractMin(minHeap);
}

// Print Huffman codes (for debugging and display)
void printCodes(MinHeapNode* root, int arr[], int top) {
    // Traverse left: assign 0
    if (root->left) {
        arr[top] = 0;
        printCodes(root->left, arr, top + 1);
    }

    // Traverse right: assign 1
    if (root->right) {
        arr[top] = 1;
        printCodes(root->right, arr, top + 1);
    }

    // If leaf node, print character and its code
    if (isLeaf(root)) {
        printf("%c: ", root->data);
        for (int i = 0; i < top; ++i)
            printf("%d", arr[i]);
        printf("\n");
    }
}

// Store Huffman codes in a 2D array for encoding
void storeCodes(MinHeapNode* root, int arr[], int top, char codes[256][MAX_TREE_HT]) {
    if (root->left) {
        arr[top] = 0;
        storeCodes(root->left, arr, top + 1, codes);
    }

    if (root->right) {
        arr[top] = 1;
        storeCodes(root->right, arr, top + 1, codes);
    }

    if (isLeaf(root)) {
        for (int i = 0; i < top; ++i) {
            codes[(unsigned char)root->data][i] = arr[i] + '0';
        }
        codes[(unsigned char)root->data][top] = '\0';
    }
}

// Compress the input file using Huffman coding (binary format)
void compressFile(const char* inputFile, const char* outputFile) {
    // Open input file for reading
    FILE* fin = fopen(inputFile, "rb");
    if (!fin) {
        printf("Error: Cannot open input file: %s\n", inputFile);
        return;
    }

    // Count frequency of each character
    int freq[256] = {0};
    int ch;
    long fileSize = 0;
    while ((ch = fgetc(fin)) != EOF) {
        freq[ch]++;
        fileSize++;
    }
    fclose(fin);

    // Collect characters that appear in the file
    char data[256];
    int charFreq[256];
    int size = 0;
    for (int i = 0; i < 256; i++) {
        if (freq[i] > 0) {
            data[size] = (char)i;
            charFreq[size] = freq[i];
            size++;
        }
    }

    if (size == 0) {
        printf("Error: File is empty\n");
        return;
    }

    // Build Huffman tree
    MinHeapNode* root = buildHuffmanTree(data, charFreq, size);

    // Generate Huffman codes
    int arr[MAX_TREE_HT], top = 0;
    char codes[256][MAX_TREE_HT] = {0};
    storeCodes(root, arr, top, codes);

    // Display Huffman code table
    printf("\nHuffman Code Table:\n");
    printf("Character -> Code\n");
    printCodes(root, arr, 0);

    // Open output file for writing compressed data in binary mode
    FILE* fout = fopen(outputFile, "wb");
    if (!fout) {
        printf("Error: Cannot create output file: %s\n", outputFile);
        return;
    }

    // Write header: number of unique characters
    fwrite(&size, sizeof(int), 1, fout);

    // Write character codes and their frequencies
    for (int i = 0; i < size; i++) {
        unsigned char c = (unsigned char)data[i];
        fwrite(&c, sizeof(unsigned char), 1, fout);
        fwrite(&charFreq[i], sizeof(int), 1, fout);
    }

    // Write original file size (needed for decompression)
    fwrite(&fileSize, sizeof(long), 1, fout);

    // Read input file again and write encoded data as bits
    fin = fopen(inputFile, "rb");
    unsigned char buffer = 0;  // Buffer to accumulate bits
    int bitCount = 0;          // Number of bits in buffer
    long totalBits = 0;        // Total bits written

    while ((ch = fgetc(fin)) != EOF) {
        // Get the code for this character
        char* code = codes[ch];

        // Write each bit of the code
        for (int i = 0; code[i] != '\0'; i++) {
            // Add bit to buffer
            buffer = (buffer << 1) | (code[i] - '0');
            bitCount++;
            totalBits++;

            // If buffer is full (8 bits), write it to file
            if (bitCount == 8) {
                fwrite(&buffer, sizeof(unsigned char), 1, fout);
                buffer = 0;
                bitCount = 0;
            }
        }
    }

    // Write remaining bits if any (pad with zeros)
    if (bitCount > 0) {
        buffer = buffer << (8 - bitCount);  // Pad with zeros
        fwrite(&buffer, sizeof(unsigned char), 1, fout);
    }

    // Write the number of padding bits at the end
    unsigned char paddingBits = (bitCount > 0) ? (8 - bitCount) : 0;
    fwrite(&paddingBits, sizeof(unsigned char), 1, fout);

    fclose(fin);
    fclose(fout);

    // Calculate and display compression statistics
    FILE* original = fopen(inputFile, "rb");
    fseek(original, 0, SEEK_END);
    long originalSize = ftell(original);
    fclose(original);

    FILE* compressed = fopen(outputFile, "rb");
    fseek(compressed, 0, SEEK_END);
    long compressedSize = ftell(compressed);
    fclose(compressed);

    printf("\nCompression Statistics:\n");
    printf("Original file size: %ld bytes\n", originalSize);
    printf("Compressed file size: %ld bytes\n", compressedSize);
    printf("Total bits encoded: %ld\n", totalBits);
    printf("Compression ratio: %.2f%%\n", (1.0 - (double)compressedSize / originalSize) * 100);
}

// Decompress the compressed file back to original (binary format)
void decompressFile(const char* inputFile, const char* outputFile) {
    // Open compressed file in binary mode
    FILE* fin = fopen(inputFile, "rb");
    if (!fin) {
        printf("Error: Cannot open compressed file: %s\n", inputFile);
        return;
    }

    // Read number of unique characters
    int size;
    fread(&size, sizeof(int), 1, fin);

    // Read character codes and frequencies
    char data[256];
    int freq[256];
    for (int i = 0; i < size; i++) {
        unsigned char c;
        fread(&c, sizeof(unsigned char), 1, fin);
        data[i] = (char)c;
        fread(&freq[i], sizeof(int), 1, fin);
    }

    // Read original file size
    long originalSize;
    fread(&originalSize, sizeof(long), 1, fin);

    // Rebuild Huffman tree
    MinHeapNode* root = buildHuffmanTree(data, freq, size);

    // Open output file for writing decompressed data
    FILE* fout = fopen(outputFile, "wb");
    if (!fout) {
        printf("Error: Cannot create output file: %s\n", outputFile);
        fclose(fin);
        return;
    }

    // Get file size to know when to stop (excluding padding byte)
    fseek(fin, 0, SEEK_END);
    long fileSize = ftell(fin);
    fseek(fin, sizeof(int) + size * (sizeof(unsigned char) + sizeof(int)) + sizeof(long), SEEK_SET);

    // Read the last byte first to get padding info
    unsigned char paddingBits;
    fseek(fin, -1, SEEK_END);
    fread(&paddingBits, sizeof(unsigned char), 1, fin);

    // Reset to data start position
    fseek(fin, sizeof(int) + size * (sizeof(unsigned char) + sizeof(int)) + sizeof(long), SEEK_SET);

    // Calculate number of data bytes (excluding header and padding byte)
    long dataBytes = fileSize - (sizeof(int) + size * (sizeof(unsigned char) + sizeof(int)) + sizeof(long) + 1);

    // Decode the compressed data bit by bit
    MinHeapNode* current = root;
    long charsWritten = 0;

    for (long byteIdx = 0; byteIdx < dataBytes; byteIdx++) {
        unsigned char byte;
        fread(&byte, sizeof(unsigned char), 1, fin);

        // Process each bit in the byte
        int bitsToProcess = 8;
        // If it's the last byte, skip padding bits
        if (byteIdx == dataBytes - 1) {
            bitsToProcess = 8 - paddingBits;
        }

        for (int bitIdx = 7; bitIdx >= 8 - bitsToProcess; bitIdx--) {
            // Extract bit at position bitIdx
            int bit = (byte >> bitIdx) & 1;

            // Traverse tree based on bit
            if (bit == 0) {
                current = current->left;
            } else {
                current = current->right;
            }

            // If leaf node reached, output character and reset to root
            if (isLeaf(current)) {
                fputc(current->data, fout);
                charsWritten++;
                current = root;

                // Stop if we've written all original characters
                if (charsWritten >= originalSize) {
                    goto done;
                }
            }
        }
    }

done:
    fclose(fin);
    fclose(fout);
    printf("Decompression completed: %s\n", outputFile);
    printf("Characters written: %ld\n", charsWritten);
}

int main(int argc, char* argv[]) {
    if (argc < 2) {
        printf("Usage:\n");
        printf("  Compress: %s -c <input_file> <compressed_file>\n", argv[0]);
        printf("  Decompress: %s -d <compressed_file> <output_file>\n", argv[0]);
        return 1;
    }

    if (strcmp(argv[1], "-c") == 0) {
        if (argc != 4) {
            printf("Error: Compression requires input file and output file\n");
            return 1;
        }
        printf("Compressing file...\n");
        compressFile(argv[2], argv[3]);
        printf("Compression completed!\n");
    } else if (strcmp(argv[1], "-d") == 0) {
        if (argc != 4) {
            printf("Error: Decompression requires compressed file and output file\n");
            return 1;
        }
        printf("Decompressing file...\n");
        decompressFile(argv[2], argv[3]);
        printf("Decompression completed!\n");
    } else {
        printf("Error: Unknown option: %s\n", argv[1]);
        printf("Use -c for compression or -d for decompression\n");
        return 1;
    }

    return 0;
}
