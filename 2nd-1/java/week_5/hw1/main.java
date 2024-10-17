import java.io.*;


public class main{

    public static void main(String[] args) throws IOException {
        // 定義 BufferedReader
        BufferedReader buffer = new BufferedReader(new InputStreamReader(System.in));

        // 使用二維陣列儲存餐點
        String[][] meals = {{"凱薩沙拉", "蒜香麵包", "炸洋蔥圈"}, {"紐約牛排", "烤雞腿排", "海鮮義大利麵"}, {"可樂", "冰檸檬茶", "咖啡"}, {"巧克力熔岩蛋糕", "奶酪", "冰淇淋聖代"}};
        // 使用二維陣列儲存價格
        int[][] prices = {{150, 100, 120}, {850, 600, 700}, {50, 60, 80}, {180, 150,170}};
        // 定義分類
        String[] category = {"前菜", "主餐", "飲品", "甜點"};
        // 定義訂單
        String order = "你選擇的餐點為: \n";
        // 定義總金額
        int total = 0;

        // 依照分類中的值逐一詢問
        for (int i = 0; i < category.length; i++) {
            // 輸出當前選則的分類
            System.out.printf("請選擇%s\n", category[i]);
            // 將菜單逐一輸出
            for (int j = 0; j < meals[i].length; j++) {
                System.out.printf("%d. %s %d\n", j + 1, meals[i][j], prices[i][j]);
            }
            // 接收用戶輸入
            int input = handleInput(buffer,  meals[i].length);
            // 格式化字串並將其加到 order 變數中
            order = order.concat(String.format("%s: %s\n", category[i], meals[i][input-1]));
            // 將價格加入 total 變數中
            total += prices[i][input-1];
        }
        // 輸出餐點內容
        System.out.printf(order);
        // 輸出價格
        System.out.printf("總價格: NT$%d", total);
    }

    // 處理用戶輸入，接受一個上限，避免超出 array index, 並將下限設為 1
    private static int handleInput(BufferedReader buffer, int upper) throws IOException {
        boolean ok = false;
        int num = 0;
        while (!ok) {
            try {
                num = Integer.parseInt(buffer.readLine());
                // 處理上下限
                if (num < 1 || num > upper+1) {
                    System.out.println("您輸入了範圍外的數字，請重新輸入");
                }
                ok = true;
            }catch (NumberFormatException e) {
                // 處理非數值
                System.out.println("您輸入的不是數字，請重新輸入");
            }
        }

        return num;
    }
}
