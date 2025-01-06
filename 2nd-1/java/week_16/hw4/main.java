import java.util.Scanner;
public class main {
    static Scanner scanner = new Scanner(System.in);
    static int count = 0;
    static Student[] students = null;
    public static void main(String[] args) {
        while (true) {
            try {
                print("請輸入資料筆數: ");
                count = scanner.nextInt();
                students = new Student[count];
                break;
            } catch (java.lang.NegativeArraySizeException e) {
                println("資料筆數不能為負");
                continue;
            } catch (java.util.InputMismatchException e) {
                println("請輸入有效整數");
                scanner.next();
                continue;
            }
        }
        for (int i = 0; i < count; i++) {
            println(String.format("請輸入第%d位學生資料", i+1));
            print("請輸入姓名: ");
            String name = scanner.next();
            print("請輸入性別: ");
            String sex = scanner.next();
            int age = handleIntInput("請輸入年齡");
            print("請輸入科系: ");
            String department = scanner.next();
            int height = handleIntInput("請輸入身高");
            int weight = handleIntInput("請輸入體重");
            students[i] = new Student(name, sex, age, department, height, weight);
        }
        while (true) {
            printMenu();
            int option = handleIntInput("請輸入功能選項");
            switch (option) {
                case 1:
                    printAll();
                    break;
                case 2:
                    while (true) {
                        try {
                            int num = handleIntInput("請輸入第n位學生");
                            println(students[num-1]);
                            break;
                        } catch (ArrayIndexOutOfBoundsException e) {
                            println("超過陣列範圍，請重新輸入");
                        }
                    }
                    break;
                case 3:
                    return;
            }
        }

    }

    public static void println(Object msg) {
        System.out.println(msg);
    }

    public static void print(Object msg) {
        System.out.print(msg);
    }

    public static void printMenu() {
        println("1. 依序顯示所有資料");
        println("2. 查詢第n筆資料");
        println("3. 離開程序");
    }

    public static int handleIntInput(Object msg) {
        while (true) {
            print(msg+": ");
            try {
                return scanner.nextInt();
            } catch (Exception e) {
                println("請輸入有效整數");
                scanner.next();
            }
        }
        
    }
    public static void printAll() {
        for (int i = 0; i < count; i++) {
            println(String.format("%d. %s", i+1, students[i].toString()));
        }
    }
}