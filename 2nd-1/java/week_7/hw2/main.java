import java.util.Scanner;
import java.util.Arrays;

public class main {
    public static void main(String[] args) {
        Scanner s = new Scanner(System.in);
        // int[] arr = {2,5,6,7,10,54};
        int[] arr = makeArray(s);
        
        System.out.println("1. 顯示排序好的陣列");
        System.out.println("2. 印出陣列內容");
        System.out.println("3. 尋找值是否存在");

        boolean keep = true;
        while (keep) {
            keep = false;
            System.out.print("請輸入選擇: ");
            String option = "";
            option = s.next();
            switch (option) {
                case "1":
                    Arrays.sort(arr);
                    showArray(arr);
                    break;
                case "2":
                    Arrays.fill(arr, 0);
                    showArray(arr);
                    break;
                case "3":
                    System.out.print("請輸入要查找的值: ");
                    int value = s.nextInt();
                    int idx = Arrays.binarySearch(arr, value);
                    String output = "有此值";
                    if (idx < 0) {
                        output = "找不到值";
                    }
                    System.out.println(output);
                    break;
                default: 
                    keep = true;
            }
        }
    }

    public static int[] makeArray(Scanner s) {
        // System.out.print("請輸入陣列長度: ");
        int length = 5;
        // length = s.nextInt();
        int[] arr = new int[length];
        for (int i = 0; i < length; i++) {
        System.out.printf("請輸入第 %d 個元素: ", i+1);
            arr[i] = s.nextInt();
        }
        return arr;
    }    
    public static void showArray(int[] arr) {
        for (int i = 0; i < arr.length; i++) {
            System.out.printf("%d ", arr[i]);
        }
    }
}