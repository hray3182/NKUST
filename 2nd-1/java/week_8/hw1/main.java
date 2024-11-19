import java.util.Scanner;
public class main {
    public static void main(String[] args) {
        print("請輸入汽車名稱: ");
        String name = handleStringInput();
        print("請輸入汽車價格: ");
        int price = handleIntInput();
        print("請輸入汽車車牌號碼: ");
        String licensePlate = handleStringInput();
        car car1 = new car(name, price, licensePlate);
        car1.showProfile();

        print("請輸入汽車名稱: ");
        String name2 = handleStringInput();
        print("請輸入汽車價格: ");
        int price2 = handleIntInput();
        print("請輸入汽車車牌號碼: ");
        String licensePlate2 = handleStringInput();
        car car2 = new car(name2, price2, licensePlate2);
        car2.showProfile();
    }

    public static String handleStringInput() {
        Scanner scanner = new Scanner(System.in);
        return scanner.nextLine();
    }

    public static int handleIntInput() {
        Scanner scanner = new Scanner(System.in);
        while (true) {
            try {
                return scanner.nextInt();
            } catch (Exception e) {
                print("請輸入數字: ");
                scanner.next();
            }
        }
    }

    public static void print(String text) {
        System.out.print(text);
    }
}