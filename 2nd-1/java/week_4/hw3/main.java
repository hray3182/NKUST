import java.io.*;

public class main {
    public static void main(String[] args) throws IOException  {
        
        int ADULT_PRICE = 589;
        int CHILD_PRICE = 369;
        
        BufferedReader buffer = new BufferedReader(new InputStreamReader(System.in));

        int adultCount, childCount, total;

        String output = "此次入場人數:";

        adultCount = handleInput(buffer, "請輸入入場成人人數");
        childCount = handleInput(buffer, "請輸入入場兒童人數");
        if (adultCount < 1 && childCount > 0) {
            System.out.println("小孩入場需家長陪同喔!");
            return;
        }
        output = output.concat(String.format(" %d 個大人,\t %d 個兒童\n", adultCount, childCount));

        total = adultCount * ADULT_PRICE + childCount * CHILD_PRICE;
        if (childCount > 0) {
            total *= 0.8;
            output = output.concat(String.format("家庭方案優惠門票總金額: %d 元", total));
            System.out.println(output);
            return;
        }

        output = output.concat(String.format("門票總金額: %d", total));

        System.out.println(output);
        
        

    }

    // 將輸入與錯誤處理封裝成函數方便重複調用
    private static int handleInput(BufferedReader buffer, String message) throws IOException {
        boolean ok = false;
        int num = 0;

        while (!ok) {
            try {
                System.out.println(message);
                String input = buffer.readLine();
                num = Integer.parseInt(input);
                if (num < 0) {
                    System.out.println("數字不可小於0");
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