import java.util.Scanner;
public class AgriSmartApp {
  public static void main(String[] args) {
    Scanner sc = new Scanner(System.in);
    InputValidator validator = new InputValidator();
    AgricultureService service = new AgricultureService();
    while (true) {
      System.out.println("\\n=== AgriSmart Java Academic Prototype ===");
      System.out.println("1 Crop demo  2 Fertilizer demo  3 Yield demo  4 Exit");
      System.out.print("Choice: "); String choice = sc.nextLine().trim();
      try {
        switch (choice) {
          case "1":
            double n=validator.readNumber(sc,"Nitrogen (0-140): ",0,140);
            double rain=validator.readNumber(sc,"Rainfall mm (20-300): ",20,300);
            System.out.println("Demonstration output: "+service.cropSuggestion(n,rain)); break;
          case "2":
            double p=validator.readNumber(sc,"Phosphorus (10-90): ",10,90);
            double k=validator.readNumber(sc,"Potassium (10-120): ",10,120);
            System.out.println("Demonstration output: "+service.fertilizerSuggestion(p,k)); break;
          case "3":
            double y=validator.readNumber(sc,"Historical yield (hg/ha): ",0,501412);
            double f=validator.readNumber(sc,"Illustrative factor (0.5-1.5): ",0.5,1.5);
            System.out.printf("Illustrative estimate: %.2f hg/ha%n",service.illustrativeYield(y,f)); break;
          case "4": System.out.println("Goodbye."); return;
          default: System.out.println("Invalid choice. Enter 1-4.");
        }
      } catch (IllegalArgumentException ex) { System.out.println("Input error: "+ex.getMessage()); }
    }
  }
}
