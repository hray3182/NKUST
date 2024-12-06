import java.util.Objects;
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

        tea tea2 = new tea("綠茶", 120, "2023-10-15", "黃色", 700);
        tea2.showProfile();
        tea2.isExpired();

        System.out.println(tea1.equals(tea2));
        // equals 是 Object 類別的方法，用於判斷兩個物件是否相等。
        // 用於判斷兩個變數引用是否指向同一個物件，
        // 因此會返回 false，因為 tea1 和 tea2 是兩個不同的物件。

        // 若是需要比較物件的內容，我們可以在物件內 override equals 方法。

    }

}