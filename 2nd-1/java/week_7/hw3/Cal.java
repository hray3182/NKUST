import java.util.Arrays;

public class Cal {
    public static void main(String[] args) {
        int leng = args.length;
        int[] arr = new int[leng];
        for (int i = 0; i < leng; i++) {
            arr[i] = Integer.parseInt(args[i]);
        }
        switch (leng) {
            case 1:
                cal(arr[0]);
                break;
            case 2:
                cal(arr[0], arr[1]);
                break;
            case 3:
                cal(arr[0], arr[1], arr[2]);
                break;
        }
    }

    public static void cal(int width) {
        System.out.printf("正方形面積: %d", width * width);
    }

    public static void cal(int height, int width) {
        System.out.printf("長方形面積: %d", height * width);
    }

    public static void cal(int side1, int side2, int side3) {
        int[] arr = {side1, side2, side3};
        if (sum(arr)- findMax(arr) <= findMax(arr)) {
            System.out.printf("不是三角形");
            return ;
        }
        double s = (double) sum(arr) / 2;
        double area = Math.sqrt(s * (s -side1 ) * (s - side2 ) * (s - side3 ));
        System.out.printf("三角形面積 %.2f", area);
    }

    public static int sum(int[] arr) {
        int sum = 0;
        for (int i = 0; i < arr.length; i++) {
            sum += arr[i];
        }
        return sum;
    }

    public static int findMax(int[] arr) {
        int max = 0;
        for (int i = 0; i < arr.length; i++) {
            if (max < arr[i]) {
                max = arr[i];
            }
        }
        return max;
    }
}