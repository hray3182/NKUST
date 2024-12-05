package Shop.user;

import Shop.shopAccount;
import Shop.util.util;

public class userAccount extends shopAccount {
    private String userName;
    private String userEmail;

    public userAccount() {
        super();
        setUserName();
        setUserEmail();
    }

    public String getUserName() {
        return userName;
    }

    public void setUserName() {
        System.out.print("請輸入姓名: ");
        userName = super.scanner.next();
    }

    public String getUserEmail() {
        return userEmail;
    }

    public void setUserEmail() {
        while (true) {
            System.out.print("請輸入信箱: ");
            String email = super.scanner.next();
            if (util.checkMail(email)) {
                userEmail = email;
                return;
            }
            System.out.println("電子郵件格式不正確，請重新輸入：");
        }
    }

    public void showProfile() {
        super.showProfile();
        System.out.printf("user name: %s\nuser email: %s\n", userName, userEmail);
        System.out.println("-------------------------------------");
    }

}