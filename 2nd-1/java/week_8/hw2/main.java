import java.util.Scanner;

public class main {
    public static void main(String[] args) {
        Car car1 = new Car();
        car1.showProfile();

        print("請輸入汽車名稱: ");
        String name = handleStringInput();
        Car car2 = new Car(name);
        car2.showProfile();

        print("請輸入汽車名稱: ");
        String name2 = handleStringInput();
        print("請輸入汽車價格: ");
        int price = handleIntInput();
        Car car3 = new Car(name2, price);
        car3.showProfile();

        print("請輸入汽車名稱: ");
        String name3 = handleStringInput();
        print("請輸入汽車價格: ");
        int price3 = handleIntInput();
        print("請輸入汽車車牌號碼: ");
        String licensePlate = handleStringInput();
        Car car4 = new Car(name3, price3, licensePlate);
        car4.showProfile();
    }

    public static String handleStringInput() {
        Scanner scanner = new Scanner(System.in);
        return scanner.nextLine();
    }   

    public static int handleIntInput() {
        Scanner scanner = new Scanner(System.in);
        return scanner.nextInt();
    }

    public static void print(String text) {
        System.out.print(text);
    }
}
