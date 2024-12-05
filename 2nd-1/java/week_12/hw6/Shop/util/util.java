package Shop.util;

import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class util {
    public static boolean checkMail(String mail) {
        String pattern = ".+@.+\\.(com|tw)";
        Pattern compiledPattern = Pattern.compile(pattern);
        Matcher matcher = compiledPattern.matcher(mail);
        return matcher.matches();
    }
}
