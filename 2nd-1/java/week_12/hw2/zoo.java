import animals.Animal;

public class zoo {
    public static void main(String[] args) {
        Animal dog = new Animal();

        dog.speak();

        // 無法編譯，protected 修飾詞使其只能在同個 package 下調用
        // 將其修飾詞改為 public
        dog.eat();

        // 無法編譯，private 修飾詞使其只能在同個 class 下調用
        // 將其修飾詞改為 public
        dog.sleep();
    }
}