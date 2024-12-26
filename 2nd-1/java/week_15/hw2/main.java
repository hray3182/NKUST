public class main {
    public static void main(String[] args) {
        Flyer f1 = new Bird("鸚鵡", "紅色");
        Flyer f2 = new Bird("老鷹", "棕色");
        Flyer f3 = new Plane("波音747", 500);
        Flyer f4 = new Plane("波音600", 600);
        Flyer f5 = new Plane("灣流A1", 1000);
        Flyer f6 = new Balloon("綠色");

        Flyer flyers[] = {f1, f2, f3, f4, f5, f6};

        for (int i = 0; i < flyers.length; i++) {
            flyers[i].fly();
        }
    }
}