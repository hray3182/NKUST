public class main {
    public static void main(String[] args){
    Object v1 = new Vehicle();
    System.out.println(v1.toString());

    Vehicle v2 = (Vehicle) v1;
    System.out.println(v2.toString());

    Car c1 = new Car();
    System.out.println(c1.toString());


    Vehicle v3 = new Vehicle("汽車", "Toyota", 120, "汽油");
    System.out.println(v3.toString());
    Car c2 = (Car) v3;
    System.out.println(c2.toString());

    }

    // (1). c1.toString() 會使用 Vehicle 的 toString 方法，結果為I am a Vehicle instance, my type is null, brand is null, speed is 0 km/h, fuel type is null
    // (2). 可以編譯，執行到 15 行會報錯，因為 Vehicle 類別無法被轉型成 Car 類別
}
