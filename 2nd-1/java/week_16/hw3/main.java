import java.util.Scanner;

public class main{
	static Scanner s = new Scanner(System.in);
	static int num1 = 0;
	static int num2 = 0;
	static String operator = "";
	static int result = 0;

	public static void main(String[] args) {
		while (true) {
			System.out.println("�п�J����");
			String expression = s.nextLine();
			String[] words = expression.split(" ");
			try {
				num1 = Integer.parseInt(words[0]);
				num2 = Integer.parseInt(words[2]);
				operator = words[1];
				switch (operator) {
					case "+":
						result = num1 + num2;
						break;
					case "-":
						result = num1 - num2;
						break;
					case "*":
						result = num1 * num2;
						break;
					case "/":
						result = num1 / num2;
						break;
					default:
						System.out.println("�z��J���B��Ť����T");
						continue;
				}
			} catch (java.lang.NumberFormatException e) {
				System.out.println("�z��J�����O���");
				continue;
			} catch (java.lang.ArrayIndexOutOfBoundsException e) {
				System.out.println("�z��J���ѼƼƶq����");
				continue;
			} catch (java.lang.ArithmeticException e) {
				System.out.println("�L�k���H0");
				continue;
			}
			System.out.printf("�B�⵲�G��%d\n", result);
			return;
		}
	}
}
