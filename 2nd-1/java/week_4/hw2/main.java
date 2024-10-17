public class main {
    public static void main(String[] args) {
        double a = 100/71*47+18-7-51*87/5+41*2/75+100;
        // the calculation from calculator is -709.1094
        // the value of a is -728

        // calculation steps: 
        // 1. 100 / 71 = 1.0
        // 2. 1.0 * 47 = 47.0
        // 3. 47.0+18 = 65.0
        // 4. 65.0-7 = 58.0
        // 5. 51*87 = 4437
        // 6. 4437/5 = 887.0
        // 7. 58.0 - 887.0 = -829.0
        // 8. 41*2 = 82
        // 9. 82/75 = 1.0
        // 10. -829+1.0 = -828.0
        // 11. -828.0+100 = -728.0

        System.out.println(a); 
    }
}