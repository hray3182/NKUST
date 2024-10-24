import java.io.*;

public class main {
    public static void main(String[] args) throws IOException {
        BufferedReader buffer = new BufferedReader(new InputStreamReader(System.in));

        String[] name = new String[5];
        int[][] score = new int[5][3];
        int min = 0, max = 100; 

        for (int i = 0; i < name.length; i++) {
            System.out.printf("請輸入第 %d 位學生的名字: ", i+1);
            name[i] = buffer.readLine();
            for (int j = 0; j < 3; j++) {
                System.out.printf("請輸入 %s 的第 %d 次成績: ", name[i], j+1);
                score[i][j] = handleIntInput(buffer);
            }
        }

        System.out.print("\n    姓名\t成績1\t成績2\t成績3\t平均\n");
        for (int i = 0; i < name.length; i++) {
            System.out.printf("%2d. %8s\t%3d\t%3d\t%3d\t%.2f\n", i+1, name[i], score[i][0], score[i][1], score[i][2], calAvg(score[i]));
        }

        int[] maxIdxs = findMaxIndex(score);
        int[] minIdxs = findMinIndex(score);

        System.out.printf("\n歷次測驗中成績最低的是 %s 的第 %d 次測驗成績，成績是 %d 分\n", name[minIdxs[0]], minIdxs[1]+1, score[minIdxs[0]][minIdxs[1]]);
        System.out.printf("歷次測驗中成績最高的是 %s 的第 %d 次測驗成績，成績是 %d 分\n", name[maxIdxs[0]], maxIdxs[1]+1, score[maxIdxs[0]][maxIdxs[1]]);

    }

    public static int handleIntInput(BufferedReader buffer) throws IOException {
        boolean ok = false;
        int num = 0;
        while (!ok) {
            try {
                num = Integer.parseInt(buffer.readLine());
                if (num < 0 || num > 100) {
                    System.out.println("您輸入的數字超過範圍，請重新輸入");
                    continue;
                }
                ok = true;
            }catch (NumberFormatException e) {
                System.out.println("您輸入的非數字，請重新輸入");
            }
        }
        return num;
    }
    
    public static double calAvg(int[] nums) {
        int total = 0;
        for (int i = 0; i < nums.length; i++) {
            total += nums[i];
        }
        return (double)total / nums.length;
    }

    public static int[] findMaxIndex(int[][] scores) {
        int max = 0, idxI = 0, idxJ = 0;
        for (int i = 0; i < scores.length; i++) {
            for (int j = 0; j < scores[i].length; j++) {
                if (scores[i][j] > max) {
                    max = scores[i][j];
                    idxI = i;
                    idxJ = j;
                }
            }
        }
        return new int[] {idxI, idxJ};
    }

    public static int[] findMinIndex(int[][] scores) {
        int min = 100, idxI = 0, idxJ = 0;
        for (int i = 0; i < scores.length; i++) {
            for (int j = 0; j < scores[i].length; j++) {
                if (scores[i][j] < min) {
                    min = scores[i][j];
                    idxI = i;
                    idxJ = j;
                }
            }
        }
        return new int[] {idxI, idxJ} ;
    }
}