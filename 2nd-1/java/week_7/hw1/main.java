import java.util.Scanner;

public class main{
    public static void main(String[] args) {
        Scanner s = new Scanner(System.in);

        
        int [] arr = makeArray(s);
        boolean ok = false;
        String option = "";
        int start = 0;
        int end = arr.length;
        
        System.out.println("1. 印出陣列全部內容");
        System.out.println("2. 印出指定索引到最後一個");
        System.out.println("3. 印出指定索引到指定索引");

        while (!ok) {
        switch (option){
            case "1":
                ok = true;
                showArray(arr);
                break;
            case "2":
                ok = true;
                boolean ok2 = false;
                while (!ok2) {
                    System.out.print("請輸入起始索引: ");
                    int input2 = s.nextInt();
                    if (input2 < 0 || input2 >= arr.length) {
                        System.out.println("超過範圍請重新輸入");
                    } else {
                        ok2 = true;
                        start = input2;   
                    }
                }
                showArray(arr, start);
                break;
            case "3":
                ok = true;
                boolean ok3 = false;
                    while(true) {

                    System.out.print("請輸入起始索引: ");
                    int input3 = s.nextInt();
                    if (input3 < 0 || input3 >= arr.length) {
                        System.out.println("超過範圍請重新輸入");
                    } else {
                        start = input3;   
                        break;
                    }
                    }
                    while(true) {

                    System.out.print("請輸入結尾索引: ");
                    int input4 = s.nextInt();
                    if (input4 < 0 || input4 >= arr.length || input4 <= start) {
                        System.out.println("超過範圍請重新輸入");
                    } else {
                        end = input4;   
                        break;
                    }

                    }
                showArray(arr, start, end);
                break;
            default:
            System.out.print("請選擇輸出方式: ");
            option = s.next();
        }
        }
    }


    public static void showArray(int []arr, int begin, int end) {
        for (int i = begin; i < end; i++) {
            System.out.println(arr[i]);
        }
    }
    public static void showArray(int []arr, int begin) {
        int end = arr.length;
        showArray(arr, begin, end);
    }
    public static void showArray(int []arr) {
        showArray(arr, 0);
    }

    public static int[] makeArray(Scanner s) {
        System.out.print("請輸入陣列長度: ");
        int length = 0;
        length = s.nextInt();
        int[] arr = new int[length];
        for (int i = 0; i < length; i++) {
        System.out.printf("請輸入第 %d 個元素: ", i+1);
            arr[i] = s.nextInt();
        }
        return arr;
    }

}