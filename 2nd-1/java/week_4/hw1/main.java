public class main {
    public static void main(String[] args) {
        // 1
        int ans1 = 60 + 10 * 10 - 8 / (7-3) + 60 / 2* 7 ;
        System.out.printf("ans1 is %d\n", ans1);
        // ans1 = 368
        // 2
        int i = 1;
        // a = 1, 先給 a 附值後 i+1
        // b = 3, 先給 i+1 後給 b 附值
        int a = i++; int b = ++i;
        // c = 3, 先給 c 附值後 i-1
        // d = 1, 先給 i-1 後給 d 附值
        int c = i--; int d = --i;
        System.out.printf("ans2: a is %d, b id %d, c is %d, d is %d\n", a, b, c, d);

        // 3
        System.out.println("ans3: ");
        double h = (8>>1)+(25<<3)-(9>>2)*(6<<1)/(5>>1);
        // h = 4 + 200 - 2 * 12 / 2 = 192
        System.out.printf("h is %.0f\n", h);
        boolean k = (67<<3>=41>>1);
        // k = (536 >= 82) = true
        System.out.printf("k is %b\n", k);
        boolean j = (91 <= 73);
        // j is false
        System.out.printf("j is %b\n", j);
    }
}