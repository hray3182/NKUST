public class Book extends Item {
    private int price;
    private int day;

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

    Book(String name, String ssn, int price,int day) {
        super(name, ssn);
        this.price = price;
        this.day = day;
    }

    public double calculateFee() {
        return price * day;
    }

    public String toString() {
        return super.toString() + String.format("價格: %d, \n租借天數: %d", price, day);
    }

    public static void main(String[] args) {
        Book b1 = new Book("test", "123", 100, 10);
        System.out.println(b1.toString());
        System.out.println(b1.calculateFee());
    }
}
