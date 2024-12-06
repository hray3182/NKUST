public class main{
    public static void main(String[] args){
        tea tea1 = new tea();

        tea1.setName("綠茶");
        tea1.setCalorie(120);
        tea1.setDate("2023-10-15");
        tea1.setColor("黃色");
        tea1.setCc(700);

        tea1.showProfile();
        tea1.isExpired();
    }
}