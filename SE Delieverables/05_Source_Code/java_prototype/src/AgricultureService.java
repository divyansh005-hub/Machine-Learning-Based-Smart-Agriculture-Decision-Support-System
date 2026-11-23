public class AgricultureService {
  // Transparent classroom rules only; these are NOT trained ML inference.
  public String cropSuggestion(double nitrogen,double rainfall) {
    if(nitrogen<40 && rainfall>150) return "Review rice suitability (rule demonstration).";
    if(rainfall<60) return "Review drought-tolerant crops (rule demonstration).";
    return "No crop selected by this simple rule; consult the ML application.";
  }
  public String fertilizerSuggestion(double phosphorus,double potassium) {
    if(phosphorus<35) return "DAP (rule demonstration).";
    if(potassium<40) return "MOP (rule demonstration).";
    return "No fertilizer selected by this simple rule; consult soil testing.";
  }
  public double illustrativeYield(double historicalYield,double factor) { return historicalYield*factor; }
}
