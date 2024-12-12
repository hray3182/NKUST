public class Vehicle {
    String type;
    String brand;
    int speed;
    String fuelType;

    Vehicle() {
        System.out.println("我是 Vehicle 的無參數建構式");
    }

    Vehicle (String type, String brand,int speed, String fuelType) {
        this.type = type;
        this.brand = brand;
        this.speed = speed;
        this.fuelType = fuelType;
    }

    public String toString() {
        return String.format("I am a Vehicle instance, my type is %s, brand is %s, speed is %d km/h, fuel type is %s", type, brand, speed, fuelType);
    }
}