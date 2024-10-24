import java.io.*;

public class main{
    public static void main(String[] args) throws IOException {
        BufferedReader buffer = new BufferedReader(new InputStreamReader(System.in));
        int len;
        char type;
        
        System.out.print("請選擇分隔線的長度: ");
        len = Integer.parseInt(buffer.readLine());

        System.out.print("請選擇分隔線的符號： ");
        type = buffer.readLine().charAt(0);
        showLine(len, type);
    }
    public static void showLine(int len, char type) {
        if (len == 0) {
            len = 15;
        }else if (len < 0) {
            len = 1;
            type = '@';
        }
        for (int i = 0; i < len; i++) {
            System.out.print(type);
        }
        System.out.print("\n");
    }
}