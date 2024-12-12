public class Car extends Vehicle {
    int seatCount;

    Car(){}

    Car(String type, String brand, int speed, String fuelType, int seatCount) {
        super(type, brand, speed, fuelType);
        this.seatCount = seatCount;
    }
}