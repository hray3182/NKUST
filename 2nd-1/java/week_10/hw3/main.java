import java.util.Scanner;

public class main {
    public static void main(String[] args) {
        
        Book book1 = new Book();
        book1.showProfile();
        Book book2 = new Book("This is book2");
        book2.showProfile();
        Book book3 = new Book("Thinking in JAVA", 1980);
        book3.showProfile();
        Book book4 = new Book("Thinking in JAVA", 2024, "Davis");
        book4.showProfile();
        Book book5 = new Book("Hello World", 1900, "Gosh", -150);
        book5.showProfile();
    }
    public static int handleIntInput() {
        Scanner s = new Scanner(System.in);
        while (true) {
            int input;
            try {
                input = s.nextInt();
                return input;
            } catch (Exception e){
                System.out.print("請輸入數字: ");
                s.nextLine();
            }
        }
    }

    public static String handleStringInput() {
        Scanner s = new Scanner(System.in);
        return s.next();
    }

    public static void print(String msg) {
        System.out.print(msg);
    }
}