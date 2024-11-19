public class main {
    public static void main(String[] args) {
        Point pointA = new Point("A", 1, 2);
        Point pointB = new Point("B", 3, 4);
        Point pointC = new Point("C", 5, 6);
        Point pointD = new Point("D", 7, 8);
        Point pointE = new Point("E", 9, 10);

        pointA.showInfo();
        pointB.showInfo();
        pointC.showInfo();
        pointD.showInfo();
        pointE.showInfo();

        Point[] points = {pointA, pointB, pointC, pointD, pointE};
        for (int i = 0; i < points.length; i++) {
            for (int j = i + 1; j < points.length; j++) {
                System.out.printf("Point %s 與 Point %s 的距離為 %.2f\n", points[i].name, points[j].name, points[i].distance(points[j]));
            }

        }
    }
}
