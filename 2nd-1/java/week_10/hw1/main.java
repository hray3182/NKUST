import java.util.Scanner;

public class main {
    public static void main(String[] args) {
        
        Book book1 = new Book();
        print("請輸入書名: ");
        book1.setBookname(handleStringInput());
        print("請輸入年份: ");
        book1.setYear(handleIntInput());
        print("請輸入作者名稱: ");
        book1.setAuthor(handleStringInput());
        print("請輸入價格: ");
        book1.setPrice(handleIntInput());

        book1.showProfile();

        Book book2 = new Book();
        print("請輸入書名: ");
        book2.setBookname(handleStringInput());
        print("請輸入年份: ");
        book2.setYear(handleIntInput());
        print("請輸入作者名稱: ");
        book2.setAuthor(handleStringInput());
        print("請輸入價格: ");
        book2.setPrice(handleIntInput());

        book2.showProfile();

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