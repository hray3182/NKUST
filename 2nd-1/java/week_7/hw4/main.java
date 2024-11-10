import java.util.Scanner;

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
                    System.out.printf("%s 您好，您的密碼是:\n%s\n ，請務必牢記您的密碼\n", newAccount, pwd);
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
}
