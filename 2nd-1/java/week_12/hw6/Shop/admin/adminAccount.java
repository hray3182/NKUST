package Shop.admin;

import Shop.shopAccount;
import Shop.util.util;

public class adminAccount extends shopAccount {
    private String adminName;
    private String adminEmail;

    public adminAccount() {
        setAdminName();
        setAdminEmail();
    }

    public String getAdminName() {
        return adminName;
    }

    public void setAdminName() {
        System.out.print("請輸入姓名: ");
        adminName = super.scanner.next();
    }

    public String getAdminEmail() {
        return adminEmail;
    }

    public void setAdminEmail() {
        while (true) {
            System.out.print("請輸入信箱: ");
            String email = super.scanner.next();
            if (util.checkMail(email)) {
                adminEmail = email;
                return;
            }
            System.out.println("電子郵件格式不正確，請重新輸入：");
        }
    }

    public void showProfile() {
        super.showProfile();
        System.out.printf("admin name: %s\nadmin email: %s\n", adminName, adminEmail);
        System.out.println("-------------------------------------");
    }
}