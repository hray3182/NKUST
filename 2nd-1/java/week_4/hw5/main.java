import java.io.*;

public class main {
    public static void main(String[] args) throws IOException {

        int count, lux;
        String quality, evalue, action;

        BufferedReader buffer = new BufferedReader(new InputStreamReader(System.in));

        count = handleNumberInput(buffer, "請輸入房間人數: ");
        lux = handleNumberInput(buffer, "請輸入房間自然光線強度: ");
        if (lux > 700) {
            quality = "佳";
            evalue = "足夠";
            action = "關閉照明";
        }else if (lux >300) {
            quality = "普通";
            evalue = "足夠";
            action = "關閉照明";
        }else{
            quality = "不佳";
            evalue = "不足";
            action = "開啟照明";
        }

        System.out.printf("[房間]\n人數:%d人\n光線強度%dLux(%s)\n光線品質: %s\n動作: %s", count, lux, quality, evalue, action);

    }

    private static int handleNumberInput(BufferedReader buffer, String msg) throws IOException {
        int num = 0;
        boolean ok = false;
        while (!ok) {
            try {
                System.out.printf(msg);
                num = Integer.parseInt(buffer.readLine());
                if (num < 0) {
                    System.out.println("數量不能低於0，請重新輸入");
                    continue;
                }
                ok = true;
            }catch (NumberFormatException e) {
                System.out.println("您輸入的非正確數字");
            }
        }
        return num;
    }
}