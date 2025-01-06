import java.util.Scanner;

public class main {
    static Appliances apps[] = {
            new Light("LED燈", "客廳",60),
            new RobotVacuum("Roomba", "臥室", 120),
            new SecurityCamera("360監控", "陽台", 80)
    };

    static String menu = "1. 查看所有家電資訊\n" + 
                        "2. 選擇家電進行操作\n" + 
                        "3. 離開程式\n";

    static Scanner scanner = new Scanner(System.in);

    public static void main(String[] args){ 
        int opt = 0;
        while (opt != 3) {
            opt = showMenu();
            if (opt == 1) {
                showAll();
            }else if(opt ==2) {
                boolean ok = false;
                int app = 0;
                while (!ok) {
                    showAllName();
                    print("請輸入要選擇操作的家電: ");
                    try {
                        app = scanner.nextInt();
                    } catch(Exception e) {
                        println("輸入錯誤請重新輸入") ;
                    }
                    if (app < 1 || app > apps.length) {
                        println("輸入錯誤請重新輸入") ;
                        continue;
                    }

                    if (apps[app-1] instanceof Operate) {
                        ((Operate)apps[app-1]).operate();
                        ok = true;
                    }else {
                        println("您選擇的電器無法操作，請重新輸入");
                    }
                }
                
            }
        }
    }

    public static void showAll() {
        for (int i = 0; i < apps.length; i++) {
            apps[i].showProfile();
        }
    }

    public static void showAllName() {
        for (int i = 0; i < apps.length; i++) {
            println(String.format("%d. %s",i+1, apps[i].getName()));
        }
    }

    public static void println(Object msg) {
        System.out.println(msg);
    }
    
    public static void print(Object msg) {
        System.out.print(msg);
    }

    public static int showMenu() {
        int opt = -1;
        while (true) {
            print(menu);
            print("請輸入: ");
            try {
                opt = scanner.nextInt();
                return opt;
            } catch(Exception e) {
                println("輸入錯誤請重新輸入") ;
            }
        }
    }

}