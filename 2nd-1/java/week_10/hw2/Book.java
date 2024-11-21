public class Book {
	private String BookName;
	private int year;
	private String Author;
	private int price;

	public String getBookName() {
		return BookName;
	}

	public void setBookname(String name) {
		this.BookName = name;	
	}

	public int getYear() {
		return year;	
	}

	public void setYear(int year) {
		this.year = year;
	}

	public String getAuthor() {
		return Author;
	}

	public void setAuthor(String author) {
		this.Author = author;
	}

	public int getPrice() {
		return (int) ((double) this.price * getDiscount());
	}

	public void setPrice(int price) {
		if (price < 0) {
			System.out.println("數字無法小於0");
			this.price = 0;
			return;
		}
		this.price = price;
	}

	public double getDiscount() {
		if (this.year <= 2010) {
			return 0.8;
		}
		return 1.0;
	}
	
	public void showProfile() {
		System.out.printf("Book Name: %s\nYear: %d\nAuthor: %s\nOriginal Price: %d\nPrice: %d\n\n", getBookName(), getYear(), getAuthor(), this.price, getPrice());
	}

	Book() {
		this("", 0, "", 0);
	}

	Book(String BookName, int year, String Author, int Price) {
		setBookname(BookName);
		setYear(year);
		setAuthor(Author);
		setPrice(Price);
	}

}