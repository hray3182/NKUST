## 1. (20 credits) A computer has 8 GB of memory. Assume each word in this computer is two bytes, how many bits are needed to address a single word in memory? If each word is four bytes, how many bits are needed to address for a single word?


### (1) 每個 word 是 2 bytes
$8GB = 8 * 2^{30} bytes $

總共有 $ 8 \times 2 ^ {30} \div 2 =2^3\times 2^{30} \div 2 = 2^{32} $ 個字

所以需要 $ \log_2 2^{31}  = 31 $ 個 bits 來儲存記憶體位置

### (2) 每個 word 是 4 bytes

$8GB = 8 * 2^{30} bytes $

總共有 $ 8 \times 2 ^ {30} \div 4 =2^3\times 2^{30} \div 2^2 = 2^{31} $ 個字

所以需要 $ \log_2 2^{31}  = 31 $ 個 bits 來儲存記憶體位置


## 2. (30 credits) An imaginary computer has 16 data registers (R0 to R15), 4096 words in memory, and 16 different instructions (add, subtract, etc). 

16 個暫存器需要 4 個 bits 來表示暫存器編號

16 個指令需要 4 個 bits 來表示指令

4096 個位置需要 12 個 bits 來表示記憶體位置

a. What is the minimum size of an add instruction in bits, if a typical instruction uses 

add 指令需要 3個暫存器，1個指令

所以需要 $4 \times 3 + 4 = 16 $ 個 bits 來表示一個 add 指令


b. What is the size of the instruction register in the computer?

加法指令需要 16 個 bits

所以需要 16 個 bits 來表示一個指令

c. What is the size of the program counter in the computer?

需要 12 個 bits 來表示記憶體位置

d. What is the size of the data bus in the computer?

每個 word 是 2 bytes

所以需要 16 個 bits 來表示一個 word

e. What is the size of the address bus in the computer?

需要 12 個 bits 來表示記憶體位置

## 3. (50 credits) Using the instruction set of the simple computer in Section 5.8, write the code for a program that performs the following calculation: C  = A - B + 1, in which A and B are integers in two’s complement format. The user needs to enter the values of A and B.

將 A 和 B 的值從鍵盤讀取到 R_0 和 R_1

(10FE)

(11FD)

將 R_0 和 R_1 相加的結果存到 R_2

(3201)

將 R_2 的值加 1 

(A200)

將 R_2 的值存到記憶體位置 M_0

(2200)
