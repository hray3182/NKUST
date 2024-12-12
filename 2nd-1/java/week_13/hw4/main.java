public class main{
    public static void main(String[] args) {
        Book b1 = new Book("b1", "b10001", 100, 10);
        print(b1.toString());
        print(b1.calculateFee());
        printLine();

        AudioBook a1 = new AudioBook("a1", "a10001", 10, 100, "SpongeBob");
        print(a1.toString());
        print(a1.calculateFee());
        printLine();

        Magazine m1 = new Magazine("m1", "m10001", 100, 10, "10");
        print(m1.toString());
        print(m1.calculateFee());
        printLine();

        DigitalMagazine d1 = new DigitalMagazine("m1", "m10001", 100, 10, "10", "PDF", "google.com/pdf/SpongeBob.pdf");
        print(d1.toString());
        print(d1.calculateFee());
        printLine();


    }

    public static void print(Object msg) {
        System.out.println(msg);
    }

    public static void printLine() {
        print("--------------------------------");
    }
}