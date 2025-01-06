public class Balloon implements Flyer{
    private String color;

    Balloon(String color) {
        setColor(color);
    }

    public void setColor(String color) {
        this.color = color;
    }

    public String getColor() {
        return this.color;
    }

    public void fly() {
        System.out.printf("%s顏色的氣球在天上飛", getColor());
    }
}