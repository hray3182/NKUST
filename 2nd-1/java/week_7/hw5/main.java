import java.util.Scanner;
import java.util.Date;
import java.text.SimpleDateFormat;

public class main {
    public static void main(String[] args) {
        String[] accounts = new String[100];
        int count = 0;
        Scanner s = new Scanner(System.in);

        boolean exit = false;

        while (!exit) {
            System.out.println("1. 創建新帳號");
            System.out.println("2. 離開");
            System.out.println("------------------------------------------");
            System.out.print("請輸入選擇: ");
            int option = s.nextInt();
            switch (option) {
                case 1:
                    boolean ok = false;
                    String newAccount = "";
                    while (!ok) {
                        System.out.print("請輸入帳號: ");
                        newAccount = s.next();
                        if (isExist(accounts, newAccount)) {
                            System.out.println("該帳號已存在");
                        } else {
                            accounts[count] = newAccount;
                            count++;
                            ok = true;
                        }
                    }

                    System.out.print("請輸入您希望的密碼長度: ");
                    int length = s.nextInt();
                    String pwd = generatePwd(length);
                    System.out.println("------------------------------------------");

                    ok = false;
                    String mail = "";
                    while (!ok) {
                        System.out.print("請輸入信箱: ");
                        mail = s.next();
                        if (isEmail(mail)) {
                            ok = true;
                        } else {
                            System.out.println("您輸入的信箱格式不對，請重新輸入");
                        }
                    }

                    Date date = new Date();
                    SimpleDateFormat format = new SimpleDateFormat("MM/dd/yyyy HH時:mm分:ss秒");

                    System.out.println("------------------------------------------");
                    System.out.printf("%s您好，歡迎您來自%s，您的註冊時間是%s，\n\n您的密碼是%s，請務必牢記。\n", newAccount, parseEmail(mail)[1], format.format(date),pwd);
                    System.out.println("------------------------------------------");
                    break;
                case 2:
                    exit = true;
                    break;
                default:
                    continue;
            }

        }

        s.close();
    }

    public static boolean isExist(String[] accounts, String account) {
        for (int i = 0; i < accounts.length; i++) {
            if (account.equals(accounts[i])) {
                return true;
            }
        }
        return false;
    }

    public static String generatePwd(int len) {
        String pwd = "";

        for (int i = 0; i < len; i++) {
            pwd += generageRandomChar();
        }
        return pwd;
    }

    public static char generageRandomChar() {
        double random = Math.random() * 94 + 33;
        return (char) (int) random;
    }

    public static boolean isEmail(String mail) {
        for (int i = 0; i < mail.length(); i++) {
            if (mail.charAt(i) == '@') {
                if (i == 0 || i == mail.length() - 1) {
                    return false;
                }
                return true;
            }
        }
        return false;
    }

    public static String[] parseEmail(String mail) {
        return mail.split("@");
    }
}
