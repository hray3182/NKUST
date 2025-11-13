# 霍夫曼編碼壓縮程式

使用霍夫曼編碼實現的無失真文本壓縮程式。

## 編譯

```bash
gcc huffman_compress.c -o huffman_compress -Wall
```

## 使用方法

### 壓縮文件
```bash
./huffman_compress -c <輸入文件> <壓縮文件>
```

### 解壓縮文件
```bash
./huffman_compress -d <壓縮文件> <輸出文件>
```

## 範例

```bash
# 壓縮
./huffman_compress -c PeterPan.txt PeterPan.bin

# 解壓縮
./huffman_compress -d PeterPan.bin PeterPan_restored.txt

# 驗證
diff PeterPan.txt PeterPan_restored.txt
```

## 測試結果

- Lyrics_GangNamStyle.txt: 1,713 bytes → 1,161 bytes (壓縮率 32.22%)
- PeterPan.txt: 284,834 bytes → 164,965 bytes (壓縮率 42.08%)
