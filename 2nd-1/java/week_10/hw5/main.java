import java.util.Scanner;

public class main {
    public static void main(String[] args) {
        Deck d = new Deck();
        d.shuffle();
        int count = 0;
        while (count < 52) {
            System.out.print("是否要發牌(Y/N): ");
            String input = handleStringInput();
            if (input.equalsIgnoreCase("Y")) {
                for (int i = 0; i < 4; i++) {
                    System.out.printf("你的第%d張牌是%s\n", count+1, d.getCard(count).String());
                    count++;
                }
            }else {
                return;
            }

        }
    }

    public static String handleStringInput() {
        Scanner s = new Scanner(System.in);
        String input = s.next();
        return input;
    }
}