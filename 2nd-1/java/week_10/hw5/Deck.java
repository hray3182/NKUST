import java.util.Random;

public class Deck {
    private Card[] cards;

    Deck() {
        this.cards = new Card[52];
        String[] numbers = {"A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"};
        int count = 0;
        
        for (int i = 0; i < 4; i++) {
            for (int j = 0; j <13; j++) {
                cards[count] = new Card(i, numbers[j]);
                count++;
            }
        }
    }

    public void print() {
        String[] suit = {"黑桃", "紅心", "菱形", "梅花"};
        for (int i = 0; i < 52; i++) {
            System.out.println(suit[cards[i].Suit] + cards[i].Number);
        }
    }

    public Card getCard(int i) {
        return this.cards[i];
    }

    public void shuffle() {
        Random random = new Random();
        for (int i = 0; i < 52; i++) {
            int swap1 = random.nextInt(52);
            int swap2 = random.nextInt(52);

            Card temp = cards[swap1];
            cards[swap1] = cards[swap2];
            cards[swap2] = temp;
        }
    }
}