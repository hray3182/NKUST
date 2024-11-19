public class Point {
    String name;
    int x;
    int y;
    double originDistance;
    
    public Point(String name, int x, int y) {
        this.name = name;
        this.x = x;
        this.y = y;
    }

    public double distance(Point point) {
        return Math.sqrt(Math.pow(x - point.x, 2) + Math.pow(y - point.y, 2));
    }

    public double distanceToOrigin() {
        return Math.sqrt(Math.pow(x, 2) + Math.pow(y, 2));
    }

    public void showInfo() {
        System.out.printf("Point %s: (%d, %d), distance to origin: %.2f\n", name, x, y, distanceToOrigin());
    }
}
