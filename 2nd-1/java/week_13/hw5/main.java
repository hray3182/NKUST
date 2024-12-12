import java.util.Scanner;
public class main{
    static Scanner s ;
    public static void main(String[] args) {
        s = new Scanner(System.in);

        // for test
        // Item b1 = new Book("b1", "b10001", 100, 10);
        // Item b2 = new Book("b2", "b10002", 100, 10);
        // Item b3 = new Book("b3", "b10003", 100, 10);

        // Item a1 = new AudioBook("a1", "a10001", 10, 100, "SpongeBob");
        // Item a2 = new AudioBook("a2", "a10002", 10, 100, "SpongeBob");

        // Item d1 = new DigitalMagazine("m1", "m10001", 100, 10, "10", "PDF", "google.com/pdf/SpongeBob.pdf");
        // Item d2 = new DigitalMagazine("m2", "m10002", 100, 10, "10", "PDF", "google.com/pdf/SpongeBob.pdf");

        // Item m1 = new Magazine("m1", "m10001", 100, 10, "10");

        Item b1 = new Book(handleNameInput(), handleSsnInput(), handlePriceInput(), handleDayInput());
        printLine();
        Item b2 = new Book(handleNameInput(), handleSsnInput(), handlePriceInput(), handleDayInput());
        printLine();
        Item b3 = new Book(handleNameInput(), handleSsnInput(), handlePriceInput(), handleDayInput());
        printLine();

        Item a1 = new AudioBook(handleNameInput(), handleSsnInput(), handlePriceInput(), handleDurationInput(), handleNarratorInput());
        printLine();
        Item a2 = new AudioBook(handleNameInput(), handleSsnInput(), handlePriceInput(), handleDurationInput(), handleNarratorInput());
        printLine();

        Item d1 = new DigitalMagazine(handleNameInput(), handleSsnInput(), handlePriceInput(), handleDayInput(), handleIssueInput(), handleFormatInput(), handleDownloadLinkInput());
        printLine();
        Item d2 = new DigitalMagazine(handleNameInput(), handleSsnInput(), handlePriceInput(), handleDayInput(), handleIssueInput(), handleFormatInput(), handleDownloadLinkInput());
        printLine();

        Item m1 = new Magazine(handleNameInput(), handleSsnInput(), handlePriceInput(), handleDayInput(), handleIssueInput());
        printLine();


        Item[] list = {b1, b2, b3, a1, a2, d1, d2, m1};

        for (int i = 0; i < list.length; i++) {
            print(list[i].toString());
            print(list[i].calculateFee());
            list[i].show();
            printLine();
        }
    }

    public static void print(Object msg) {
        System.out.println(msg);
    }

    public static void printLine() {
        print("--------------------------------");
    }

    public static String getStringInput(String field) {
        System.out.printf("請輸入%s: ", field);
        return s.next();
    } 

    public static int getIntInput(String field) {
        System.out.printf("請輸入%s: ", field);
        int num = s.nextInt();
        return num;
    } 


    public static String handleNameInput() {
        return getStringInput("書名");
    }

    public static String handleSsnInput() {
        return getStringInput("SSN編號");
    }

    public static String handleNarratorInput() {
        return getStringInput("旁白");
    }

    public static String handleDownloadLinkInput() {
        return getStringInput("下載連結");
    }

    public static String handleFormatInput() {
        return getStringInput("格式");
    }

    public static String handleIssueInput() {
        return getStringInput("期刊");
    }

    public static int handleDayInput() {
        return getIntInput("租借日期");
    } 

    public static int handlePriceInput() {
        return getIntInput("價格");
    }

    public static int handleDurationInput() {
        return getIntInput("時長");
    }
}
