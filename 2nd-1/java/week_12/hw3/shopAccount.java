public class shopAccount {
    static int KeyID;
    private int UID;
    private String account;
    private String password;

    public String getAccount() {
        return account;
    }

    public void  setAccount(String account) {
        this.account = account;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public void showProfile() {
        System.out.println("Account info: ");
        System.out.printf("UID: %d\nAccount: %s\nPassword: %s\n\n", UID, account, password);
    }

    shopAccount(String account, String password) {
        KeyID++;
        this.UID = KeyID;
        setAccount(account);
        setPassword(password);
    }
}