public class People {
    private double weight;
    private String gender;
    private double alcoholAmount;
    private double hours;
    private double BAC;

    public People(double weight, String gender){
        this.weight = weight;
        this.gender = gender;
    }

    public void calculateBAC(){
        double rate = 0.68;
        if (gender.equals("male")){
            rate = 0.55;
        }
        BAC = (alcoholAmount / (weight * rate));
        System.out.printf("BAC: %.2f\n", BAC);
    }

    public void drink(Alcohol alcohol, double hours){
        this.alcoholAmount += alcohol.getAlcoholAmount();
        this.hours = hours;
    }

    public void calculateRestTime(){
        double rate = 0.015;
        double currentBAC = BAC - (rate * hours);
        if (currentBAC > 0.05){        
            double time = (currentBAC - 0.05) / rate;
            System.out.printf("Rest time: %.2f hours", time);
        } else {
            System.out.println("You can drive now");
        }
    }
}