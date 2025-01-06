import java.util.Scanner;

public class main{
	static Scanner s = new Scanner(System.in);
	static int num1 = 0;
	static int num2 = 0;
	static String operator = "";
	static int result = 0;

	public static void main(String[] args) {
		while (true) {
			System.out.println("請輸入公式");
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
						System.out.println("您輸入的運算符不正確");
						continue;
				}
			} catch (java.lang.NumberFormatException e) {
				System.out.println("您輸入的不是整數");
				continue;
			} catch (java.lang.ArrayIndexOutOfBoundsException e) {
				System.out.println("您輸入的參數數量不對");
				continue;
			} catch (java.lang.ArithmeticException e) {
				System.out.println("無法除以0");
				continue;
			}
			System.out.printf("運算結果為%d\n", result);
			return;
		}
	}
}
