

public class Cal         
{
    public static void main(String args[])
    {
        
	int result=0;  
	try {

		switch(args[1].charAt(0)){  
		case '+':	  
		result = Integer.parseInt(args[0]) + Integer.parseInt(args[2]);
		System.out.println("�B�⵲�G�O" + result);	  
		break;
		case '-':	  
		result = Integer.parseInt(args[0]) - Integer.parseInt(args[2]);
		System.out.println("�B�⵲�G�O" + result);
			break;
		case 'x':	  
		result = Integer.parseInt(args[0]) * Integer.parseInt(args[2]);
		System.out.println("�B�⵲�G�O" + result);
		break;         
		case '/':	  
		result = Integer.parseInt(args[0]) / Integer.parseInt(args[2]); 
		System.out.println("�B�⵲�G�O" + result);
		break;
		default:
			System.out.println(args[1] + " �O�L�Ī��B���! �L�k�B��"); 
		}
	} catch (java.lang.NumberFormatException e) {
		System.out.println("�z��J�����O���");
		return;
	} catch (java.lang.ArithmeticException e) {
		System.out.println("���Ƥ��ର0");
		return;
	} catch (java.lang.ArrayIndexOutOfBoundsException e) {
		System.out.println("�ѼƼƶq����");
		return;
	}
	}
}    


