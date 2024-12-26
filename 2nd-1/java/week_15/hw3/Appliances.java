public abstract class Appliances{
    private String type;
    private String name;
    private String location;
    private int consumption;

    public String getType() {
        return this.type;
    }

    public void setType(String type) {
        this.type = type;
    }

    public String getName() {
        return this.name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getLocation() {
        return this.location;
    }

    public void setLocation(String location) {
        this.location = location;
    }

    public int getConsumption() {
        return this.consumption;
    }

    public void setConsumption(int consumption) {
        this.consumption = consumption;
    }

    Appliances(String type, String name, String location, int consumption) {
        setType(type);
        setName(name);
        setLocation(location);
        setConsumption(consumption);
    }

    public abstract void showProfile();
}