import java.util.Scanner;

public class main{
    public static void main(String[] args) {
        Scanner s = new Scanner(System.in);
        System.out.println("請輸入您的年齡");
        int age = 0;
        try {
            age = s.nextInt();
        }catch (NumberFormatException e){
            System.out.println("您的輸入有誤，終止程序");
            return;
        }catch (java.util.InputMismatchException e) {
            System.out.println("您的輸入有誤，終止程序");
            return;
        }
        System.out.printf("您的年齡為%d", age);
        
    }
}