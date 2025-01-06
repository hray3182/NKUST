public class SecurityCamera extends Appliances implements Operate{
    private boolean status = false;
    SecurityCamera(String name, String location, int consumption) {
        super("SecurityCamera", name, location, consumption);
    }

   public void showProfile() {
        System.out.printf("type: %s ,name: %s, location: %s, consumption: %dW\n", getType(), getName(), getLocation(), getConsumption());
    }

    public void operate() {
        String msg = "";
        if (status) {
            msg = String.format("stop camera");
        } else {
            msg = String.format("start camera");
        }
        System.out.println(msg);
        status = !status;
    }

    public static void main(String[] args) {
        SecurityCamera s = new SecurityCamera("cam", "bathroom", 50);
        s.showProfile();
        s.operate();
        s.operate();
    }
}