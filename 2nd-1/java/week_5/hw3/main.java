import java.io.*;

public class main {
    public static void main(String[] args) throws IOException {
        // 創建BufferedReader
        BufferedReader buffer = new BufferedReader(new InputStreamReader(System.in));
        int age = 0;
        double first, loan = 0.0;

        // 跑迴圈直到用戶輸入的貸款金額大於等於0
        do {
            System.out.printf("請輸入貸款金額(大於等於0): ");
            first = (double) Integer.parseInt(buffer.readLine()); 
            loan = first; 
        } while (!(loan >= 0));

        // 跑迴圈直到用戶輸入的貸款總年數大於0
        do {
            System.out.printf("請輸入貸款總年數(至少1年): ");
            age = Integer.parseInt(buffer.readLine()); // 讀取用戶輸入並轉換為int
        } while (!(age > 0));

        // 計算每年的利息，假設年利率為1.5%
        for (int i = 0; i < age; i++) {
            loan *= 1.015; // 每年增加1.5%的利息
        }

        // 輸出最終需要還款的本金和利息
        System.out.printf("您在%d年後需要還款本金加利%.2f元(本金為%.2f元、利息為%.2f元)", age, loan, first, loan - first);
    }
}
