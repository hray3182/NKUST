public class Magazine extends Item{
    private int price;
    private int day;
    private String issue;

    public void setPrice(int price) {
        this.price = price;
    }

    public int getPrice() {
        return this.price;
    }

    public void setDay(int day) {
        this.day = day;
    } 

    public int getDay() {
        return this.day;
    }

    public void setIssue(String issue) {
        this.issue = issue;
    }

    public String getIssue() {
        return this.issue;
    }

    public double calculateFee() {
        return price * day * 0.9;
    }

    public String toString() {
        return super.toString() + String.format("價格: %d, \n租借天數: %d\n期數: %s\n", price, day, issue);
    }

    public Magazine(String name, String ssn, int price, int day, String issue) {
        super(name, ssn);
        this.price = price;
        this.day = day;
        this.issue = issue;
    }

    public static void main(String[] args) {
        Magazine m1 = new Magazine("test", "123", 100, 10, "10");
        System.out.println(m1.toString());
        System.out.println(m1.calculateFee());
    }

}