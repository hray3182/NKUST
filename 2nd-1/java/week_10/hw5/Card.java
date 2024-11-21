public class Card {
    int Suit;
    String Number;

    Card(int suit, String number) {
        this.Suit = suit;
        this.Number = number;
    }

    public String String() {
        String[] suit = {"黑桃", "紅心", "菱形", "梅花"};
        return String.format("%s %s", suit[this.Suit], this.Number);
    }
}