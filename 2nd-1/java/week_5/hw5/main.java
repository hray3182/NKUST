import java.io.*;

public class main {
    public static void main(String[] args) throws IOException {
        // 定義data array
        String[] data = new String[4]; 

        // 定義身高、體重變數
        int weight, height;

        // 創建 BufferedReader
        BufferedReader buffer = new BufferedReader(new InputStreamReader(System.in));

        // 要求輸入名字
        System.out.print("請輸入姓名: ");
        data[0] = buffer.readLine();
        data[0] = "姓名: ".concat(data[0]);

        // 要求輸入身高
        System.out.print("請輸入身高: ");
        height = handleNumberInput(buffer, 0, 300);
        // 要求輸入體重
        System.out.print("請輸入體重: ");
        weight= handleNumberInput(buffer, 0, 500);
        data[1] = String.format("身高: %d", height);
        data[2] = String.format("體重: %d", weight);
        data[3] = String.format("BMI %.2f", weight / ((height / 100.0) * (height / 100.0)));
        for (int i = 0; i < data.length; i++) {
            System.out.println(data[i]);
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
