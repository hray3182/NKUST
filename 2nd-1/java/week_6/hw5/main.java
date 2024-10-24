import java.io.*;

public class main {
    public static void main(String[] args) throws IOException {
        BufferedReader buffer = new BufferedReader(new InputStreamReader(System.in));
        int numOfStudents = 0;
        String[] subjects = { "國文", "英文", "微積分", "程式設計", "計算機概論", "物理" };
        int[] weights = { 1, 1, 1, 1, 1, 1 };

        System.out.print("請輸入學生人數: ");
        numOfStudents = handleIntInput(buffer, 1000, 1);

        String[] students = new String[numOfStudents];
        int[][] scores = new int[numOfStudents][6];
        int[] totalOfScores = new int[numOfStudents];
        double[] subjectsAvg = new double[subjects.length];
        int[]maxValueIdxInSubjects = new int[subjects.length];
        String[][] lowerThanAvg = new String[subjects.length][students.length];

        for (int i = 0; i < numOfStudents; i++) {
            System.out.printf("請輸入第 %d 位學生的名字: ", i + 1);
            students[i] = buffer.readLine();
            printHrMsg(String.format("請輸入%s的成績", students[i]));
            for (int j = 0; j < subjects.length; j++) {
                System.out.printf("請輸入%s成績: ", subjects[j]);
                scores[i][j] = handleIntInput(buffer, 100, 0);
            }
        }

        printHrMsg("請輸入各科權重");
        for (int i = 0; i < subjects.length; i++) {
            System.out.printf("請輸入%s權重: ", subjects[i]);
            weights[i] = handleIntInput(buffer, 100, 1);
        }

        // 計算加權總分
        for (int i = 0; i < numOfStudents; i++) {
            totalOfScores[i] = calTotal(scores[i], weights);
        }

        // 計算各科平均分數
        subjectsAvg = calSubjectAvgs(scores);

        // 找出低於平均分的學生
        lowerThanAvg = findLowerThanAvgStudents(students, scores, subjectsAvg);

        // 取得各科成績最高者
        maxValueIdxInSubjects = findMaxValueIdxInSubject(scores);

        boolean ok = true;

        while (ok) {
            printHrMsg("請選擇您想要執行的功能");
            System.out.println("(1) 印出結果");
            System.out.println("(2) 每一個學生的加權後的總成績");
            System.out.println("(3) 每一項考科的平均分");
            System.out.println("(4) 取出該考科最高成績的學生");
            System.out.println("(5) 低於該科平均的所有學生");
            System.out.println("(6) 離開");
            String input = buffer.readLine();

            switch (input) {
                case "1":
                    printResult(students, scores);
                    break;
                case "2":
                    printTotal(students, totalOfScores);
                    break;
                case "3":
                    printAvg(students, scores);
                    break;
                case "4":
                    printHighestGrade(subjects, students, maxValueIdxInSubjects);
                    break;
                case "5":
                    printLowerAvgsStudent(subjects, lowerThanAvg);
                    break;
                case "6":
                    ok = false;
                    break;
            }

        } 

    }

    public static int handleIntInput(BufferedReader buffer, int upper, int lower) throws IOException {
        boolean ok = false;
        int num = 0;
        while (!ok) {
            try {
                num = Integer.parseInt(buffer.readLine());
                if (num < lower || num > upper) {
                    System.out.println("您輸入的數字超過範圍，請重新輸入");
                    continue;
                }
                ok = true;
            } catch (NumberFormatException e) {
                System.out.println("您輸入的非數字，請重新輸入");
            }
        }
        return num;
    }

    public static void printHrMsg(String msg) {
        System.out.printf("----------%s----------\n", msg);
    }

    public static int calTotal(int[] score, int[] weights) {
        int total = 0;
        for (int i = 0; i < score.length; i++) {
            total += score[i] * weights[i];
        }
        return total;
    }

    public static double calAvg(int[] score) {
        int total = 0;
        for (int i = 0; i < score.length; i++) {
            total += score[i];
        }
        return (double) total / score.length;
    }

    public static double[] calSubjectAvgs(int[][] scores) {
        double[] avgs = new double[scores[0].length];

        for (int i = 0; i < scores.length; i++) {
            for (int j = 0; j < scores[i].length; j++) {
                avgs[j] += (double) scores[i][j];
            }
        }

        for (int i = 0; i < avgs.length; i++) {
            avgs[i] /= (double) scores.length;
        }

        return avgs;
    }

    public static int[] findMaxValueIdxInSubject(int[][] scores) {
        int[] maxs = new int[scores[0].length];
        int[] idxs = new int[scores[0].length];

        // 初始化
        for (int i = 0; i < maxs.length; i++) {
            maxs[i] = 0;
        }

        for (int i = 0; i < scores.length; i++) {
            for (int j = 0; j < scores[i].length; j++) {
                if (scores[i][j] > maxs[j]) {
                    maxs[j] = scores[i][j];
                    idxs[j] = i;
                }
            }
        }

        return idxs;
    }

    public static String[][] findLowerThanAvgStudents(String[] students, int[][] scores, double[] avgs) {
        String[][] lowerThanAvg = new String[avgs.length][students.length];
        for (int i = 0; i < scores[0].length; i++) {
            int count = 0;
            for (int j = 0; j < scores.length; j++) {
                if (scores[j][i] < avgs[i]) {
                    lowerThanAvg[i][count] = students[j];
                    count++;
                }
            }
        }
        return lowerThanAvg;
    }

    public static void printLowerAvgsStudent(String[] subjects, String[][] lowerThanAvg) {
        for (int i = 0; i < subjects.length; i++) {
            System.out.printf("%s：", subjects[i]);
            for (int j = 0; j < lowerThanAvg[i].length && lowerThanAvg[i][j] != null; j++) {
                System.out.printf("%s ", lowerThanAvg[i][j]);
            }
            System.out.println();
        }
    }

    public static void printResult(String[] students, int[][] scores) {
        System.out.printf("%-13s%-13s%-13s%-12s%-11s%-10s%-13s\n", "學生", "國文", "英文", "微積分", "程式設計", "計算機概論", "物理");
        for (int i = 0; i < scores.length; i++) {
            System.out.printf("%-15s", students[i]);
            for (int j = 0; j < scores[i].length; j++) {
                System.out.printf("%-15d", scores[i][j]);
            }
            System.out.print("\n");
        }
    }

    public static void printTotal(String[] students, int[] scores) {
        System.out.printf("%-13s%-11s\n", "學生", "加權成績");
        for (int i = 0; i < students.length; i++) {
            System.out.printf("%-15s%-15d\n", students[i], scores[i]);
        }
    }

    public static void printAvg(String[] students, int[][] scores) {
        System.out.printf("%-13s%-11s\n", "學生", "平均成績");
        for (int i = 0; i < students.length; i++) {
            System.out.printf("%-15s%-13.2f\n", students[i], calAvg(scores[i]));
        }
        System.out.print("\n");
    }

    public static void printHighestGrade(String[] subjects, String[] students, int[] idx) {
        System.out.printf("%-13s%-13s%-12s%-11s%-10s%-13s\n",  "國文", "英文", "微積分", "程式設計", "計算機概論", "物理");

        for (int i = 0; i < subjects.length; i++) {
            System.out.printf("%-15s", students[idx[i]]);
        }
        System.out.print("\n");
    }
}
