public class main {
    public static void main(String[] args){
    Vehicle v1 = new Vehicle();
    System.out.println(v1.toString());
    }

    // 1. 可以輸出，會印出 Vehicle@59f95c5d，輸出結果來自於 java.lang.Object 的方法，是繼承於 object 的方法。
    // 2. 結果為 I am a Vehicle instance, my type is null, brand is null, speed is 0 km/h, fuel type is null
    // 由於 object 的 toString 被 Vehicle 中的 toString override，所以調用的是方法中 toString，結果就與 (1) 不同

}
