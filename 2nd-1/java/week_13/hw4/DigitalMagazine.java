public class DigitalMagazine extends Magazine {
    private String format;
    private String downloadLink;

    public double calculateFee() {
        return getDay() * getPrice() * 0.8;
    }
public String toString() {
        return super.toString() + String.format("電子書格式: %s\n下載連結: %s\n", format, downloadLink);
    }

    DigitalMagazine(String name, String ssn, int price, int day, String issue, String format, String downloadLink) {
        super(name, ssn, price, day, issue);
        this.format = format;
        this.downloadLink = downloadLink;
    }

    static public void main(String[] args) {
        DigitalMagazine d = new DigitalMagazine("test", "123", 100, 10, "10", "PDF", "google.com/download/hello_world.pdf");
        System.out.println(d.toString());
        System.out.println(d.calculateFee());
    }
}