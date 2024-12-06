public class Alcohol {
    private int volume;
    private double alcoholPercentage;
    private double alcoholAmount;

    public Alcohol(int volume, double alcoholPercentage){
        this.volume = volume;
        this.alcoholPercentage = alcoholPercentage;
        this.alcoholAmount = volume * alcoholPercentage;
    }

    public void showProfile(){
        System.out.println("容量：" + volume + "ml");
        System.out.println("酒精濃度：" + alcoholPercentage * 100 + "%");
        System.out.println("酒精量：" + alcoholAmount + "ml");
    }

    public int getVolume(){
        return volume;
    }

    public void setVolume(int volume){
        this.volume = volume;
        this.alcoholAmount = volume * alcoholPercentage;
    }

    public double getAlcoholPercentage(){
        return alcoholPercentage;
    }

    public void setAlcoholPercentage(double alcoholPercentage){
        this.alcoholPercentage = alcoholPercentage;
        this.alcoholAmount = volume * alcoholPercentage;
    }

    public double getAlcoholAmount(){
        return alcoholAmount;
    }
}
