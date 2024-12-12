public class AudioBook extends Item {
    private int price;
    private int duration;
    private String narrator;

    public void setPrice(int price) {
        this.price = price;
    }

    public int getPrice() {
        return price;
    }

    public void setDuration(int duration) {
        this.duration = duration;
    }

    public int getDuration() {
        return this.duration;
    }

    public void setNarrator(String narrator) {
        this.narrator = narrator;
    }

    public String getNarrator() {
        return this.narrator;
    }

    public double calculateFee() {
        return price * duration;
    }

    public String toString() {
        return super.toString() + String.format("價格: %d(分), \n時長: %d\n旁白: %s\n", price, duration, narrator);
    }

    AudioBook(String name, String ssn, int price, int duration, String narrator) {
        super(name, ssn);
        setPrice(price);
        setDuration(duration);
        setNarrator(narrator);
    }

    public static void main(String[] args) {
        AudioBook a = new AudioBook("test", "123", 10, 10, "John");
        System.out.println(a.toString());
        System.out.println(a.calculateFee());
    }
}