# 離散數學 ch1 homework

## 1. 64 bit
1. 可以表多少整數？ $2^{64}$
2. 可以代表多少正整數及負整數？
        
正整數: $2^{63}-1$
        
負整數: $2^{63}$
        

---

## 2. 某校學生之學號格式為□□□□□□□□□共九碼，每一碼均為0\~9之任一個數字。前三碼為入學之民國年度、第四碼為學制別、第五碼與第六碼為系所代碼、第七碼為班級別 ( 只能0\~4 )、最後兩碼則為該班級內之流水號。

1. 最多有多少種不同的學制？ $10種$
2. 最多有幾個系所？ $99個$
3. 一個系所最多有幾班？ $5個班$
    又最多有幾位學生？ $500個$
4. 一個班級最多有幾位學生？ $100個$
5. 104學年度入學的學生最多有幾人？ $10\times10\times10\times4\times10\times10=400,000$
    最多又可分成幾班？ $4000$
    

---

## 3. 程式設計期末上機考試題目有A、B、C三份試卷。每份試卷均涵蓋了基礎概念、邏輯指令、迴圈、陣列、輸出入指令、指標、函數、綜合應用等類別的題目。三份試卷各類別題目之數量如下表。每位同學可自由選擇其中一份試卷做答，且每類別題目必須挑選一題做答。

| 試卷 | 基礎概念 | 邏輯指令 | 迴圈 | 陣列 | 輸出入指令 | 指標 | 函數 | 綜合應用 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| A | 6 | 4 | 8 | 4 | 5 | 5 | 4 | 4 |
| B | 6 | 5 | 4 | 5 | 4 | 5 | 6 | 4 |
| C | 4 | 6 | 6 | 3 | 5 | 4 | 5 | 6 |


(1). 有幾種作答法？
    
    
$A卷:6\times4\times8\times4\times5\times5\times4\times4=307,200$
    
$B卷: 6\times5\times4\times5\times4\times5\times6\times4=288,000$
    
$C卷:4\times6\times6\times3\times5\times4\times5\times6=259,200$
    
$307,200+288,000+259,200=854,400$
    
(2). 某生選了A卷，有幾種做答法？ $307,200$

(3). 某生選了B卷，有幾種做答法？ $288,000$

(4). 某生選了C卷，有幾種做答法？ $259,200$

---

## 4. 某筆記型電腦 ( 筆電 ) 製造廠所生產的筆電有8種LCD螢幕尺寸、10種外殼顏色、8種CPUs、6種RAM的容量、6種不同容量的硬碟，及3種不同協定的無線網卡等可供選配。

(1). 共有多少款不同的筆電可供消費者選擇？ $8\times10\times8\times6\times6\times3=69,120$

(2). 某甲欲購買8 GB RAM的該廠牌筆電，有多少款可供其選擇？ $69,120\div6=11,520$

(3). 可生產多少款配備17吋寬螢幕且硬碟容量為2 TB的筆電？ $69,120\div8\div6=1,440$

---

## 5. 寫出 $\{a, b, c,d,e\}$ 的所有排列
    
    [a b c d e]
    [a b c e d]
    [a b d c e]
    [a b d e c]
    [a b e d c]
    [a b e c d]
    [a c b d e]
    [a c b e d]
    [a c d b e]
    [a c d e b]
    [a c e d b]
    [a c e b d]
    [a d c b e]
    [a d c e b]
    [a d b c e]
    [a d b e c]
    [a d e b c]
    [a d e c b]
    [a e c d b]
    [a e c b d]
    [a e d c b]
    [a e d b c]
    [a e b d c]
    [a e b c d]
    [b a c d e]
    [b a c e d]
    [b a d c e]
    [b a d e c]
    [b a e d c]
    [b a e c d]
    [b c a d e]
    [b c a e d]
    [b c d a e]
    [b c d e a]
    [b c e d a]
    [b c e a d]
    [b d c a e]
    [b d c e a]
    [b d a c e]
    [b d a e c]
    [b d e a c]
    [b d e c a]
    [b e c d a]
    [b e c a d]
    [b e d c a]
    [b e d a c]
    [b e a d c]
    [b e a c d]
    [c b a d e]
    [c b a e d]
    [c b d a e]
    [c b d e a]
    [c b e d a]
    [c b e a d]
    [c a b d e]
    [c a b e d]
    [c a d b e]
    [c a d e b]
    [c a e d b]
    [c a e b d]
    [c d a b e]
    [c d a e b]
    [c d b a e]
    [c d b e a]
    [c d e b a]
    [c d e a b]
    [c e a d b]
    [c e a b d]
    [c e d a b]
    [c e d b a]
    [c e b d a]
    [c e b a d]
    [d b c a e]
    [d b c e a]
    [d b a c e]
    [d b a e c]
    [d b e a c]
    [d b e c a]
    [d c b a e]
    [d c b e a]
    [d c a b e]
    [d c a e b]
    [d c e a b]
    [d c e b a]
    [d a c b e]
    [d a c e b]
    [d a b c e]
    [d a b e c]
    [d a e b c]
    [d a e c b]
    [d e c a b]
    [d e c b a]
    [d e a c b]
    [d e a b c]
    [d e b a c]
    [d e b c a]
    [e b c d a]
    [e b c a d]
    [e b d c a]
    [e b d a c]
    [e b a d c]
    [e b a c d]
    [e c b d a]
    [e c b a d]
    [e c d b a]
    [e c d a b]
    [e c a d b]
    [e c a b d]
    [e d c b a]
    [e d c a b]
    [e d b c a]
    [e d b a c]
    [e d a b c]
    [e d a c b]
    [e a c d b]
    [e a c b d]
    [e a d c b]
    [e a d b c]
    [e a b d c]
    [e a b c d]
    

---

## 6. 某資管系有26位專任老師，依專長劃分如下：數學4人、資訊9人、管理6人、通訊7人。今需要8位老師組成課程委員會。

(1). 任意挑選，有幾種方法？ $C_8^{26}=\frac{26\times25\times24\times23\times22\times21\times20\times19}{8\times7\times6\times5\times4\times3\times2}=1,562,275$

(2). 各領域均挑兩位老師，有幾種方法？
    $C^4_2\times C^9_2 \times C^6_2 \times C^7_2=6\times36\times15\times21=68,040$
    
(3). 資訊領域的老師至少2位，有幾種方法？
        
        
所有可能扣掉只有1位與2位資訊老師的case

#### case 1: 只有一位資訊老師

$C^4_1\times C^{4+6+7}_7 = 4 \times C^{17}_7=4 \times 19,448 = 777,92$
        
#### case: 2 只有二位資訊老師

$C^4_2 \times C^{17}_6=6\times 12,376 = 74,256$

加總: 

$1,562,275-77,792-74,256=1,410,227$#

        
(4). 數學與資訊專長的老師加起來最多4位，有幾種方法？
        
有 5 個 case 要處理：
        
- 加起來 0 位 $C^{13}_8=1,287$
- 加起來 1 位 $C^{13}_7 \times C^{13}_1= 1,716\times13=22,308$
- 加起來 2 位 $C^{13}_6\times C^{13}_2=1,716\times78=133,848$
- 加起來 3 位 $C^{13}_5 \times C^{13}_3=1,287\times286=368,082$
- 加起來 4 位 $C^{13}_4\times C^{13}_4=715\times 715=511,225$
        
$1,287+22,308+133,848+368,082+511,225=1,036,750$
        
## 7. 接續前一題，再回答以下問題。
(1). 資訊專長的老師最多4位，有幾種方法？
- 0位 $C^{17}_8=24,310$
- 1位 $C^{17}_7 \times C^9_2=12,376\times 36 = 445,536$
- 2位 $C^{17}_6 \times C^9_3=6,188 \times 84 = 519,792$
- 3位 $C^{17}_5 \times C^9_4=2,380 \times 126 = 299,880$
- 4位 $C^{17}_4 \times C^9_5=680 \times 126 = 85,680$
       
$24,310+445,536+519,792+299,880+85,680=1,375,198$

(2). 管理專長的老師至少2位、但通訊老師最多2位，有幾種方法？
- 至少 2 位管理老師： $\binom{6}{2} = 15$
- 至少 3 位管理老師： $\binom{6}{3} = 20$
- 至少 4 位管理老師： $\binom{6}{4} = 15$
- 至少 5 位管理老師： $\binom{6}{5} = 6$
- 至少 6 位管理老師： $\binom{6}{6} = 1$
- 最多 2 位通訊老師： $\binom{7}{2} = 21$
- 最多 1 位通訊老師： $\binom{7}{1} = 7$
- 最多 0 位通訊老師： $\binom{7}{0} = 1$
        
2 位管理老師 2位通訊老師: $\binom{13}{4}\times15\times 21 = 715\times15\times21=225,225$

2 位管理老師 1位通訊老師: $\binom{13}{5}\times15\times 7=1,287\times15\times7=135,135$

2 位管理老師 0位通訊老師: $\binom{13}{6}\times15\times1=1,716\times15\times1=25,740$

3 位管理老師 2位通訊老師: $\binom{13}{3}\times20\times21=286\times20\times21=120,120$

3 位管理老師 1位通訊老師: $\binom{13}{4}\times20\times7=715\times20\times7=100,100$

3 位管理老師 0位通訊老師: $\binom{13}{5}\times20\times1=1,287\times20=25,740$

4 位管理老師 2位通訊老師: $\binom{13}{2}\times15\times21=78\times15\times21=24,570$

4 位管理老師 1位通訊老師: $\binom{13}{3}\times15\times7=286\times15\times7=30,030$

4 位管理老師 0位通訊老師: $\binom{13}{4}\times15\times1=715\times15\times1=10,725$

5 位管理老師 2位通訊老師: $\binom{13}{1}\times6\times21=1,638$

5 位管理老師 1位通訊老師: $\binom{13}{2}\times6\times7=3,276$

5 位管理老師 0位通訊老師: $\binom{13}{3}\times6\times1=1,716$

6 位管理老師 2位通訊老師: $21$

6 位管理老師 1位通訊老師: $\binom{13}{1}\times7=78$

6 位管理老師 0位通訊老師: $\binom{13}{2}\times1=78$

全部加在一起
    
$225,225+135,135+25,740+120,120+100,100+25,740+24,570+30,030+10,725$
$+1,638+3,276+1,716+21+78+78=705,192$
    
(3). 資訊與管理這兩個領域的人數必須相等，另兩個領域則至少1位，有幾種方法？
- 資訊與管理各0位 $\binom{11}{8}=165$
- 資訊與管理各1位 $\binom{6}{1}\times\binom{9}{1}\times\binom{11}{6}-\binom{7}{6}=24,941$
- 資訊與管理各2位 $\binom{6}{2}\times\binom{9}{2}\times\binom{11}{4}-\binom{4}{4}-\binom{7}{4}=178,164$
- 資訊與管理各3位 $\binom{6}{3}\times\binom{9}{3}\times\binom{11}{2}-\binom{4}{2}-\binom{7}{2}=92,366$
- 加總 $165+24,941+178,164+92,366=295,636$

---

## 8. 計算以下結果，並試著推廣出任意正整數 的結果。

(1). $\binom{2}{0}+2\times\binom{2}{1}+2^2\times\binom{2}{2}=1+2\times2+4\times1=9$

(2). $\binom{3}{0}+2\times\binom{3}{1}+2^2\times\binom{3}{2}+2^3\times\binom{3}{3}=1+2\times3+4\times3+8\times1=27$

(3). $\binom{4}{0}+2\times\binom{4}{1}+2^2\times\binom{4}{2}+2^3\times\binom{4}{3}+2^4\times\binom{4}{4}$
    $=1+2\times4+4\times6+8\times6+16\times1=97$

(4). $\binom{5}{0}+2\times\binom{5}{1}+2^2\times\binom{5}{2}+2^3\times\binom{5}{3}+2^4\times\binom{5}{4}+2^5\times\binom{5}{5}$
$=1+2\times5+4\times10+8\times10+16\times5+32\times1=243$

---

## 9. 寫出從{a,b,c}選4個的所有組合，每個物件均可被重複選取。

```
aaaa
aaab
aaac
aaba
aabb
aabc
aaca
aacb
aacc
abaa
abab
abac
abba
abbb
abbc
abca
abcb
abcc
acaa
acab
acac
acba
acbb
acbc
acca
accb
accc
baaa
baab
baac
baba
babb
babc
baca
bacb
bacc
bbaa
bbab
bbac
bbba
bbbb
bbbc
bbca
bbcb
bbcc
bcaa
bcab
bcac
bcba
bcbb
bcbc
bcca
bccb
bccc
caaa
caab
caac
caba
cabb
cabc
caca
cacb
cacc
cbaa
cbab
cbac
cbba
cbbb
cbbc
cbca
cbcb
cbcc
ccaa
ccab
ccac
ccba
ccbb
ccbc
ccca
cccb
cccc
```

---

## 10. 某電腦的主記憶體 (RAM) 的位址匯流排 (address bus) 有48-bit，假設每個byte均給一個位址，該電腦RAM的容量有多大？
$2^{48}bytes\div2^{40}bytes(1TB)=2^8TB=256TB$

---

## 11. $x_1+x_2+x_3<15$ 有幾組可能的解？所有變數均是非負的整數。
 
原式 $=x_1+x_2+x_3<=14$
 
可以寫成 $x_1+x_2+x_3+x_4=14$

所以求 $\binom{14+4-1}{4-1}=\binom{17}{3}=680$

---

## 12. $x_1+x_2+x_3\leq15, x_1\geq2,x_2,x_3\geq0$ 有幾組可能的整數解？

$(z_1+2)+x_2+x_3\leq15, z_1=x_1-2$

$z_1+x_2+x_3\leq13$

$\binom{13+4-1}{4-1}=\binom{16}{3}=560$

---

## 13. 證明定理1.11並用 $\binom{10}{4}$ 來驗證。

### 定理1.11
    
(1). $$\binom{n}{r}=\sum_{j=r}^{n}\binom{j-1}{r-1}$$

使用組合法證明

$$\binom{10}{4}=\sum_{j=4}^{10}\binom{j-1}{3}$$

左邊可以理解成從從有著1-10編號的10顆球裡面選出4顆球

右邊可以理解成先將預選第 j 顆球，再從編號1~(j-1)顆球裡面選出3顆球，並將所有組合加總，結果應該與左邊相等。

$\binom{3}{3}=1$

$\binom{4}{3}=4$

$\binom{5}{3}=10$

$\binom{6}{3}=20$

$\binom{7}{3}=35$

$\binom{8}{3}=56$

$\binom{9}{3}=84$

加總 $1+4+10+20+35+56+84=210$

$\binom{10}{4}=210$

等式成立

(2). $$\binom{n}{r}=\sum_{j=0}^n\binom{n-1-(r-j)}{j}$$
    
使用遞迴帕斯卡等式證明
$\binom{10}{4}=\binom{9}{4}+\binom{9}{3}=\binom{9}{4}+\binom{8}{3}+\binom{8}{2}=\binom{9}{4}+\binom{8}{3}+\binom{7}{2}+\binom{7}{1}=\binom{9}{4}+\binom{8}{3}+\binom{7}{2}+\binom{6}{1}+\binom{6}{0}$
$=\binom{9}{4}+\binom{8}{3}+\binom{7}{2}+\binom{6}{1}+\binom{5}{0}$

$=\sum_{j=0}^{4}\binom{5+j}{j}=\sum_{j=0}^{10}\binom{10-1-(4-j)}{j}$

## 14. 證明若 $n$ 為非負的整數，則

使用組合法證明
$$\binom{2n}{n}=\sum_{j=0}^n\binom{n}{j}^2$$

左邊為從 2n 個相異物中取出 n 個物品的可能性
右邊可以理解為將 2n 個相異物平分成 2 堆，分別從裡面取出 j 個物品與 n-j 的組合，又因為 $\binom{n}{n-j}=\binom{n}{j}$ ，最後將每個 j 個可能性加總，組合數量會與等式左邊的結果一樣。

因此得證 $\binom{2n}{n}=\sum_{j=0}^n\binom{n}{j}^2$

## 15. 用 $\binom{17}{5}=\binom{9+8}{5}$來驗證范德蒙等式。

$\binom{17}{5}=6188$
$\binom{9}{0}\binom{8}{5}=56$
$\binom{9}{1}\binom{8}{4}=630$
$\binom{9}{2}\binom{8}{3}=2016$
$\binom{9}{3}\binom{8}{2}=2352$
$\binom{9}{4}\binom{8}{1}=1008$
$\binom{9}{5}\binom{8}{0}=126$

加總
$56+630+2016+2352+1008+126=6188$

等式成立

## 16. 證明
$$\binom{n}{0}2^n-\binom{n}{1}2^{n-1}+\binom{n}{2}2^{n-2}-\cdots+(-1)^n\binom{n}{n}=1, n\geq1$$

原式可以寫成
$$\binom{n}{0}2^n(-1)^0+\binom{n}{1}2^{n-1}(-1)^1+\binom{n}{2}2^{n-2}(-1)^2\cdots+\binom{n}{n}2^0(-1)^n$$

根據二項式定理上式為 $(2-1)^n$ ，1任何次方都為1，原式成立

## 17.  $(x+y+z+w)^{10}$展開後 $x^2yz^3w^4$ 的係數為何？

根據多項式定理 $\frac{n!}{(n_1)!(n_2)!\cdots(n_k)!}$

$x^6yz^3w^4$ 的係數為 $\frac{10!}{2!1!3!4!}=\frac{10\times9\times8\times7\times6\times5}{2\times3\times2}=12600$

## 18. $(2x^3+y-2z^2+w^2)^{10}$展開後 $x^6yz^6w^8 $的係數為何？

另 $a=2x^3, b=2z^2, c=w^2$，根據上題 $a^2yz^3w^4$的係數為12600

$12600\times2^3\times(-2)^2=403,200$

## 19. 令 $n=4k $， $n$ 與 $k$ 皆為正整數。證明 $\frac{n!}{(4!)^k}$ 一定是整數。

原式 $=\frac{(4k)!}{(4!)^k}=\frac{(4k)!}{24^k}$

將 $(4k)!$ 展開，可以獲得 $k$ 組四個數一組的算式
$(4k)(4k-1)(4k-2)(4k-3) (4k-4)(4k-5)(4k-6)(4k-7)\cdots4\times3\times2\times1$

因為是連續數字，所以每組一定都可以被24整除，所以可以將以上算式寫成
$$24^k\times m$$

m表示剩餘的部份

因此

$$\frac{24^k\times m}{24^k} = m$$

m 顯然是一個整數，一所以原式成立

## 20. 證明 $\frac{(3n)!}{2^n\times3^n}$一定是整數， $n$ 為正整數。
原式 $=\frac{(3n)!}{6^n}$
根據上題，可將其寫成 $\frac{6^k\times m}{6^n}=m$

m 顯然為整數，等式成立