public class RobotVacuum extends Appliances implements Operate{

    private boolean status;

    RobotVacuum(String name, String location, int consumption) {
        super("Robot Vacuum", name, location, consumption);
    }

    public void showProfile() {
        System.out.printf("type: %s ,name: %s, location: %s, consumption: %dW\n", getType(), getName(), getLocation(), getConsumption());
    }

    public void operate() {
        if (status) {
            System.out.printf("%s stop clean.\n", getName());
        } else {
            System.out.printf("%s start clean.\n", getName());
        }

        status = !status;
    }

    public static void main(String[] args) {
        RobotVacuum r = new RobotVacuum("A1", "livingroom", 100);
        r.showProfile();
        r.operate();
        r.operate();
    }
}