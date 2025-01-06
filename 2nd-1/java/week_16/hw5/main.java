import java.util.Scanner;

public class main {
    public static int quotien(int number1, int number2) {
        if (number2 == 0) {
            throw new ArithmeticException("Cannot div by 0");
        }
        return number1 / number2;
    }

    public static void main(String[] args) {
        Scanner input = new Scanner(System.in);

        while (true) {

            System.out.print("Enter two integers\n");

            int num1 = input.nextInt();
            int num2 = input.nextInt();
            int result = 0;
            try {
                result = quotien(num1, num2);
                System.out.printf("%d / %d is %d", num1, num2, result);
                return;
            } catch (Exception e) {
                System.out.println(e.getMessage());
            }
        }
    }
}