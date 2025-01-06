public class Vehicle {
    private String name;
    private double speed;

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return this.name;
    }

    public void setSpeed(double speed) {
        this.speed = speed;
    }

    public double getSpeed() {
        return this.speed;
    }

    public String toString() {
        return String.format("name: %s, speed: %.2f", this.name, this.speed);
    }

    Vehicle(String name, double speed) {
        setName(name);
        setSpeed(speed);
    }

    public static void main(String[] args) {
        Vehicle v = new Vehicle("test", 1.565);
        System.out.println(v.toString());
    }

}