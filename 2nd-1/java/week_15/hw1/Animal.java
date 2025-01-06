public class Animal{
    private String name;
    private String color;

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return this.name;
    }

    public void setColor(String color) {
        this.color = color;
    }

    public String getColor() {
        return this.color;
    }

    Animal(String name, String color) {
        setName(name);
        setColor(color);
    }

    public String toString() {
        return String.format("name: %s, color: %s\n", name, color);
    }

    public static void main(String[] args) {
        Animal a = new Animal("test", "color");
        System.out.println(a.toString());
    }
}
