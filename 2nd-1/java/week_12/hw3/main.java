import java.util.Scanner;

public class main {
    public static void main(String[] args) {
        Scanner s = new Scanner(System.in);
        while (true) {

            println("請輸入帳號: ");
            String account = s.next();
            println("請輸入密碼: ");
            String password = s.next();
            new shopAccount(account, password).showProfile();
            println("是否繼續輸入?(y/n)");
            String option = s.next();
            if (!option.equals("y")) {
                return;
            }
            println("");
        }
    }

    static public void println(String msg) {
        System.out.println(msg);
    }
}