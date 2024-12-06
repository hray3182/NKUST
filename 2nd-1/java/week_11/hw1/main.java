public class main{
    public static void main(String[] args){
        tea tea1 = new tea();

        tea1.setName("tea1");
        tea1.setCalorie(100);
        tea1.setDate("2024-12-06");
        tea1.setColor("black");
        tea1.setCc(100);

        tea1.showProfile();
        tea1.isExpired();

        // (1) 為何 tea 物件會有 showProfile 和 isExpired 方法？
        // 因為 tea 繼承了 drink 類別，所以 tea 物件會有 drink 類別的方法。

        // (2) 請問 showProfile() 和 isExpired() 方法的執行結果？內容值是怎麼來的？
        // showProfile() 的執行結果會顯示 tea 物件的屬性值。
        // isExpired() 的執行結果會顯示 tea 物件的日期是否過期。
        // 內容值當調用 tea 物件的 set 方法時，若是 tea 物件不包含該屬性但 drink 有，則會使用 drink 的方法。

    }
}