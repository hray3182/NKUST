public class main {
    public static void main(String[] args){
    Object v1 = new Vehicle();
    System.out.println(v1.toString());

    Vehicle v2 = (Vehicle) v1;
    System.out.println(v2.toString());
    }
    // (1). 可以執行 toString, 執行的是 Vehicle 中的 toString 方法
    // (2). 不能執行，需強制轉型。因為編譯器只知道 v1, v2 在字面上是不同類別，所以編譯不了。使用轉型才能讓編譯器通過編譯。
}
