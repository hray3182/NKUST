public class Bird extends Animal implements Flyer{
    Bird(String name, String color) {
        super(name, color);
    }

    public void fly() {
        System.out.printf("%s is flying on the sky.\n", getName());
    }

    static public void main(String[] args) {
        Bird b = new Bird("bird", "red");
        b.fly();
    }
}