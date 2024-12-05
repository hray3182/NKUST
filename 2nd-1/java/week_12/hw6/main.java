import Shop.*;
import Shop.admin.adminAccount;
import Shop.user.userAccount;
import java.util.Scanner;

public class main {
    public static void main(String[] args) {
        Scanner s = new Scanner(System.in);
        System.out.println("使用者帳號");
        while (true) {
            new userAccount().showProfile();
            println("是否繼續輸入?(y/n)");
            String option = s.next();
            if (!option.equals("y")) {
                break;
            }
            println("");
        }

        System.out.println("管理員帳號");
        while (true) {
            new adminAccount().showProfile();
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