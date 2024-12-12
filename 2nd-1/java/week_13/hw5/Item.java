public abstract class Item{
    private String name;
    private String ssn;

    public void setNname(String name) {
        this.name = name;
    }

    public String getName() {
        return this.name;
    }

    public void setSsn(String ssn) {
        this.ssn = ssn;
    }

    public String getSsn() {
        return this.ssn;
    }

    abstract double calculateFee();

    public String toString() {
        return String.format("書名: %s\n書籍編號: %s\n", this.name, this.ssn);
    }

    public Item(String name, String ssn) {
        setNname(name);
        setSsn(ssn);
    }

    public void show() {
        System.out.printf("%s-%s\n", name, ssn);
    }

}