# 14 homework

1. 有 20 個資料 1、2、3、4、5、6、7、8、9、10、11、12、13、14、15、16、17、18、19、20，請利用二元搜尋法找尋 2、13、18 須花費多少次。

    - 2:  3次
    - 13: 3次
    - 18: 3次


2. 何謂雜湊? 並敘述與一般搜尋技巧之差異。

雜湊是透過一組函數，將資料轉換成 index，能夠快速找到資料。

3. 略述雜湊函數有幾種? 及其解決碰撞的方法。

    - 除留餘數法
    - 摺疊法
    - 數字分析法
    - 平方取中法

    碰撞解決方法：
    - 線性開放位址
    - 鏈結串列

4. 假設有一雜湊表有 26 個桶，每桶有 2 個槽。今有 10 個資料 { HD, E, K, H, J, B2, B1, B3, B5, M } 存在雜湊表裡。若使用的雜湊函數 f(x) = ORD(X 的第一個字母) % 26，求：
   (a) 裝載因子為多少?  

    - 裝載因子 = 資料數 / 總槽數 = $ 10 / 26 * 2 \approx 0.1923$

   (b) 發生多少次的碰撞?及幾次的溢位。  

    - $f(H) = 20,$: HD 與 H碰撞 +1
    - $f(B) = 14,$: B1, B2, B3, B5 碰撞 +3

   碰撞次數 = 4
   
   (c) 假若發生溢位的處理方式為線性開放位址，請畫出處理後雜湊表的內容。  

   | 索引 | 資料    |
   |------|---------|
   | 14   | B2, B1  |
   | 15   | B3      |
   | 16   | B5      |
   | 17   | E       |
   | 20   | HD, H   |
   | 22   | J       |
   | 23   | K       |
   | 25   | M       |
   
   (d) 同(c)，但處理的方式為鏈結串列。

   | 索引 | 資料 |
   |------|------|
   | 14   | B2 → B1 → B3 → B5 |
   | 17   | E |
   | 20   | HD → H |
   | 22   | J |
   | 23   | K |
   | 25   | M |
