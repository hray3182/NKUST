import java.util.Scanner; 

public class main{
    public static void main(String[] args) {
        Scanner s = new Scanner(System.in);

        System.out.println("請輸入員工資訊:[姓名,職位,年資] [姓名,職位] [姓名,年資]");
        String[] arguments = s.next().split(",");
        if (arguments.length == 3) {
            int year = Integer.parseInt(arguments[2]);
            Employee e1 = new Employee(arguments[0], arguments[1], year);
            e1.showProfile();
            return ;
        }


        try {
            int year = 0;
            year =  Integer.parseInt(arguments[1]);
            Employee e3 = new Employee(arguments[0], year);
            e3.showProfile();
        }catch (Exception e) {
            Employee e2 = new Employee(arguments[0], arguments[1]);
            e2.showProfile();
        }
    }
}