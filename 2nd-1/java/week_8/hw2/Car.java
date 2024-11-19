public class Car {
    String name;
    int price;
    String licensePlate;

    public Car() {
    }

    public Car(String name) {
        this.name = name;
    }

    public Car(String name, int price) {
        this.name = name;
        this.price = price;
    }

    public Car(String name, int price, String licensePlate) {
        this.name = name;
        this.price = price;
        this.licensePlate = licensePlate;
    }

    public void showProfile() {
        System.out.println("汽車名稱: " + name);
        System.out.println("汽車價格: " + price);
        System.out.println("車牌號碼: " + licensePlate);
    }
}

