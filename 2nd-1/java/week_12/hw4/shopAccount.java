import java.util.Scanner;
public class shopAccount {
    static int KeyID;
    private int UID;
    final private String account = setAccount();
    private String password;

    static Scanner scanner = new Scanner(System.in);

    public String getAccount() {
        return account;
    }

    public String setAccount() {
        System.out.print("請輸入帳號: ");
        return scanner.next();
    }

    public String getPassword() {
        return password;
    }

    public void setPassword() {
        while (true) {

        System.out.print("請輸入密碼: ");
        String password1 = scanner.next();

        System.out.print("請再次輸入密碼確認: ");
        String password2 = scanner.next();

        if (password1.equals(password2)) {
            this.password = password1;
            return;
        }
        System.out.println("密碼不一致，請重新輸入");
        }
    }

    public void showProfile() {
        System.out.println("-------------------------------------");
        System.out.println("Account info: ");
        System.out.printf("UID: %d\nAccount: %s\nPassword: %s\n", UID, account, password);
        System.out.println("-------------------------------------");
    }

    shopAccount() {
        KeyID++;
        UID = KeyID;
        setPassword();
    }
}