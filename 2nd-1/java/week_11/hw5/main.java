public class main {
    public static void main(String[] args) {
        Alcohol bear = new Alcohol(500, 0.06);
        System.out.println("啤酒");
        bear.showProfile();

        People people = new People(70, "male");
        people.drink(bear, 1);
        people.calculateBAC();
        people.calculateRestTime();
    }

    public static Alcohol mixer(Alcohol alcohol1, Alcohol alcohol2){
        int totalVolume = alcohol1.getVolume() + alcohol2.getVolume();
        double totalAlcoholPercentage = (alcohol1.getAlcoholAmount() + alcohol2.getAlcoholAmount()) / totalVolume;
        return new Alcohol(totalVolume, totalAlcoholPercentage);
    }
}
