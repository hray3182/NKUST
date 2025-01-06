public class Plane extends Vehicle implements Flyer{
    Plane(String name, double speed) {
        super(name, speed);
    }

    public void fly() {
        System.out.printf("%s is flying on the sky. speed: %.2f km/h\n", getName(), getSpeed());
    }

    public static void main(String[] args) {
        Plane p = new Plane("747", 500);
        p.fly();
    }
}