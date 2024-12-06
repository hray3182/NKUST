public class main {
    public static void main(String[] args) {
        Alcohol bear = new Alcohol(500, 0.06);
        System.out.println("啤酒");
        bear.showProfile();

        Alcohol wine = new Alcohol(750, 0.12);
        System.out.println("紅酒");
        wine.showProfile();

        Alcohol spirit = new Alcohol(300, 0.4);
        System.out.println("烈酒");
        spirit.showProfile();

        Alcohol mixed = mixer(wine, spirit);
        System.out.println("混合酒");
        mixed.showProfile();
    }

    public static Alcohol mixer(Alcohol alcohol1, Alcohol alcohol2){
        int totalVolume = alcohol1.getVolume() + alcohol2.getVolume();
        double totalAlcoholPercentage = (alcohol1.getAlcoholAmount() + alcohol2.getAlcoholAmount()) / totalVolume;
        return new Alcohol(totalVolume, totalAlcoholPercentage);
    }
}
