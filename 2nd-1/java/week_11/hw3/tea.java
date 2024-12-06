import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class tea extends drink {
    private String color;
    private int cc;

    public String getColor(){
        return this.color;
    }

    public void setColor(String color){
        this.color = color;
    }

    public int getCc(){
        return this.cc;
    }

    public void setCc(int cc){
        this.cc = cc;
    }

    public void isExpired() {
        try {
            SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
            Date productDate = sdf.parse(getDate());
            Date currentDate = new Date();
            System.out.printf("%s-%s-%dcc is ", getName(), getColor(), getCc());
            if (productDate.before(currentDate)) {
                System.out.println("expired");
            } else {
                System.out.println("not expired");
            }
        } catch (ParseException e) {
            System.out.println("Invalid date format");
        }
    }

    public void showProfile(){
        super.showProfile();
        System.out.println("Color: " + getColor());
        System.out.println("Cc: " + getCc());
    }

    public tea(String name, int calorie, String date, String color, int cc){
        super(name, calorie, date);
        this.color = color;
        this.cc = cc;
    }

    public tea(){
        super();
        this.color = "";
        this.cc = 0;
    }
}
