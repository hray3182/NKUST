import java.util.Scanner;

public class Student {
    static Scanner scanner = new Scanner(System.in);
    String name;
    String sex;
    int age;
    String department;
    int height;
    int weight;
    Student(String name, String sex, int age, String department, int height, int weight) {
        this.name = name;
        this.sex = sex;
        this.age = age;
        this.department = department;
        this.height = height;
        this.weight = weight;
    }

    public String toString() {
        return String.format("name: %s, sex: %s, age: %d, department %s, height: %d, weight: %d", name, sex, age, department, height, weight);
    }
}