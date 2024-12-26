public class Light extends Appliances {
    Light(String name, String location, int consumption) {
        super("Light", name, location, consumption);
    }

    public void showProfile() {
        System.out.printf("type: %s ,name: %s, location: %s, consumption: %dW\n", getType(), getName(), getLocation(), getConsumption());
    }

    public static void main(String[] args) {
        Light l = new Light("test", "room", 10);
        l.showProfile();
    }
}