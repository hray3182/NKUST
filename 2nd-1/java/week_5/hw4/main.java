import java.io.*;

public class main {
    public static void main(String[] args) throws IOException {
        // 定義商品
        String[] items = {"沙發", "椅子", "桌子", "玻璃杯"};
        // 定義價格
        int[] prices = {7000, 499, 759, 58};
        // 定義預算 
        int budget = 0 ;
        // 定義訂單
        String order = "總共購買了:\n";
        // 定義總計
        int total = 0;

        // 創建 BufferedReader
        BufferedReader buffer = new BufferedReader(new InputStreamReader(System.in));

        // 要求使用者輸入預算
        System.out.print("輸入購買預算金額: ");
        budget = handleNumberInput(buffer, budget, Integer.MAX_VALUE);

        // 定義一個狀態變數表示是否繼續購物
        boolean keep = true;
        while(keep) {
            System.out.println("請輸入要購買的品項: ");
            // 列出商品
            for (int i = 0; i < items.length; i++) {
                System.out.printf("(%d) %s %d元/個\n", i+1, items[i], prices[i]);
            }
            // 取得購買品項
            int selected = handleNumberInput(buffer, 0, items.length );
            // 這裡-1對應array idx
            selected--;
            // 取得數量
            System.out.printf("請輸入要購買%s的數量: ", items[selected]);
            int quantity = handleNumberInput(buffer, 0, Integer.MAX_VALUE);
            // 將數量乘上價格加到總計
            total += quantity * prices[selected];
            // 將購買記錄寫入order
            order = order.concat(String.format("%s: %d個\n", items[selected], quantity));
            // 詢問使用者是否要繼續購買
            System.out.print("是否還要購買上述選項中的其它商品(Y/N): ");
            keep = buffer.readLine().equals("Y");
        }
        // 將購買記錄輸出
        System.out.print(order);
        // 輸出總金額
        System.out.printf("總金額: %d\n", total);
        // 若是總金額大於預算則輸出提醒
        if (total > budget) {
            System.out.printf("超出預算，超出%d元", total - budget);
        }

    }

    // 定義一個函數用於處理關於數字的input
    private static int handleNumberInput(BufferedReader buffer, int lower, int upper) throws IOException{
        boolean ok = false;
        int num = 0;
        while(!ok) {
            try {
                num = Integer.parseInt(buffer.readLine());
                if (num < lower || num > upper) {
                    System.out.println("您輸入的數字超過範圍，請重新輸入");
                    continue;
                }
                ok = true;
            }catch(NumberFormatException e) {
                System.out.println("您輸入的不是數字，請重新輸入");
            }
        }
        return num;
    }
}
