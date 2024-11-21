public class Employee {
    private String name;
    private String position;
    private int year;
    private int money;

    public void setName(String name) {
        this.name = name;
    }

    public String getName() {
        return this.name;
    }

    public void setPosition(String position) {
        String[] positions = {"一般員工", "主管", "部長"};
        for (int i = 0; i < positions.length; i++) {
            if (positions[i].equals(position)) {
                this.position = position;
                return;
            }
        }
        this.position = "一般員工";
    }

    public String getPosition() {
        return this.position;
    }

    public void setYear(int year) {
        if (year >= 0 && year < 16) {
            this.year = year;
            return;
        }
        this.year = 1;
    }

    public int getYear() {
        return this.year;
    }

    public void setMoney() {
        int money = 22000;
        switch (this.position) {
            case "主管" :
                money = 40000;
                break;
            case "部長": 
                money = 55000;
                break;
        }

        this.money = money + calculateBonus();
    }

    public int getMoney() {
        return this.money;
    }

    public int calculateBonus() {
        if (this.year <= 5) {
            return 2000;
        }

        if (this.year <= 10) {
            return 6000;
        }

        return 12000;
            
    }

    public void showProfile() {
        System.out.println("員工資訊:");
        System.out.printf("姓名: %s, 職位: %s, 年資: %d, 月薪: %d\n\n", getName(), getPosition(), getYear(), getMoney());
    }

    Employee(String name, String position, int year) {
        setName(name);
        setPosition(position);
        setYear(year);
        setMoney();
    }

    Employee(String name, int year) {
        this(name, "", year);
    }

    Employee(String name, String position) {
        this(name, position, 1);
    }
}
