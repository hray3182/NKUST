public class car {
    private String name;
    private int price;
    private String licensePlate;

    public car(String name, int price, String licensePlate) {
        setName(name);
        setPrice(price);
        setLicensePlate(licensePlate);
    }

    public String getName() {
        return name;
    }

    public int getPrice() {
        return price;
    }

    public String getLicensePlate() {
        return licensePlate;
    }

    public void setName(String name) {
        this.name = name;
    }

    public void setPrice(int price) {
        this.price = price;
    }

    public void setLicensePlate(String licensePlate) {
        this.licensePlate = licensePlate;
    }

    public void showProfile() {
        System.out.println("汽車名稱: " + name);
        System.out.println("汽車價格: " + price);
        System.out.println("車牌號碼: " + licensePlate);
    }
}
