import java.io.*;
public class main{
    public static void main(String[] args) throws IOException {
        int elderCount, youthCount, totalCount, income;
        double taxRate;
        BufferedReader buffer = new BufferedReader(new InputStreamReader(System.in));
        
        elderCount = handleNumberInput(buffer, "請輸入家庭中老年人的人數: ");
        youthCount = handleNumberInput(buffer, "請輸入家庭中青年人的人數: ");
        income = handleNumberInput(buffer, "請輸入家庭年收入（元）: ");

        totalCount = elderCount + youthCount;

        if (income <= 1000000) {
            taxRate = 0.1;
        }else if (income <= 1500000) {
            taxRate = 0.15;
        }else if (income <= 2000000) {
            taxRate = 0.2;
        }else {
            taxRate = 0.3;
        }

        if (totalCount > 0 && income / totalCount < 15000) {
            taxRate = 0.0;
        }

        taxRate -= 0.04 * elderCount;

        if (taxRate < 0) {
            taxRate = 0;
        }

        System.out.printf("家庭人數組成: 老年人 %d 人，青年人 %d 人，總人數 %d 人\n", elderCount, youthCount, totalCount);
        System.out.printf("稅率: %.0f%%\n", taxRate*100);        
        System.out.printf("所得稅總額: %.1f", taxRate * income);
        
    }

    private static int handleNumberInput(BufferedReader buffer, String msg) throws IOException {
        int num = 0;
        boolean ok = false;
        while (!ok) {
            try {
                System.out.printf(msg);
                num = Integer.parseInt(buffer.readLine());
                // handle negetiva num
                if (num < 0) {
                    System.out.println("數字不得小於零");
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