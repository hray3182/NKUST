import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;

public class drink {
    private String name;
    private int calorie;
    private String date;

    public drink(){
        this.name = "";
        this.calorie = 0;
        this.date = "";
    }

    public drink(String name, int calorie, String date){
        this.name = name;
        this.calorie = calorie;
        this.date = date;
    }

    public void setName(String name){
        this.name = name;
    }

    public String getName(){
        return this.name;
    }

    public void setCalorie(int calorie){
        this.calorie = calorie;
    }

    public int getCalorie(){
        return this.calorie;
    }

    public void setDate(String date){
        this.date = date;
    }

    public String getDate(){
        return this.date;
    }

    public void showProfile() {
        System.out.println("Name: " + this.name);
        System.out.println("Calorie: " + this.calorie);
        System.out.println("Date: " + this.date);
    }

    public void showExpired() {
        try {
            SimpleDateFormat sdf = new SimpleDateFormat("yyyy-MM-dd");
            Date productDate = sdf.parse(this.date);
            Date currentDate = new Date();
            
            if (productDate.before(currentDate)) {
                System.out.println("Expired");
            } else {
                System.out.println("Not expired");
            }
        } catch (ParseException e) {
            System.out.println("Invalid date format");
        }
    }
}
