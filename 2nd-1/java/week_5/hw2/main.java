import java.io.*;

public class main {
    public static void main(String[] args) throws IOException {

        // 定義 BufferedReader
        BufferedReader buffer = new BufferedReader(new InputStreamReader(System.in));

        // 定義人數、總分、及格人數
        int numOfPeo, total = 0, numOfPass = 0;
        // 先取得學生人數
        numOfPeo = handleInput(buffer, "請輸入學生的數量: ", (int)2<<16);
        // 根據學生人數跑迴圈，要求使用者逐一輸入成績
        for (int i = 0; i < numOfPeo; i++) {
            int input = handleInput(buffer, String.format("請輸入第 %d 位學生的分數: ", i + 1), 100);
            // 將成績加總到 total 變數中
            total += input;
            // 若是及格則將 numOfPass 變數 +1
            if (input >= 60) {
                numOfPass++;
            }
        }
        // 定義平均數儲存計算結果
        double average = total / numOfPeo;
        // 輸出分均分數
        System.out.printf("班上的平均分數為: %.1f\n", average);
        // 輸出及格人數
        System.out.printf("及格的學生人數為: %d", numOfPass);
    }

    // 用於處理用戶輸入，接收 msg 用於提示用戶輸入，接收 upper 設定 input 的最大值
    private static int handleInput(BufferedReader buffer, String msg, int upper) throws IOException {
        boolean ok = false;
        int num = 0;
        while (!ok) {
            try {
                System.out.printf("%s", msg);
                num = Integer.parseInt(buffer.readLine());
                // 將最小值設為 1
                if (num < 0 || num > upper) {
                    System.out.println("您輸入的數字超過範圍，請重新輸入");
                    continue;
                }
                ok = true;
            } catch (NumberFormatException e) {
                System.out.println("您輸入的不是數字，請重新輸入");
            }
        }
        return num;
    }
}