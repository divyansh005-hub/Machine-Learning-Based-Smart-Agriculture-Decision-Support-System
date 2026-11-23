import java.util.Scanner;
public class InputValidator {
  public double readNumber(Scanner sc,String prompt,double min,double max) {
    System.out.print(prompt); String raw=sc.nextLine().trim(); double value;
    try { value=Double.parseDouble(raw); }
    catch(NumberFormatException ex) { throw new IllegalArgumentException("Enter a numeric value."); }
    if(!Double.isFinite(value)||value<min||value>max)
      throw new IllegalArgumentException("Value must be between "+min+" and "+max+".");
    return value;
  }
}
