package preprocessing;

public class ExtendedStringEntry  {
	private StringEntry stringEntry;
	
	private double hi14Score;
	private double venekatesanScore;
	private double yu11Score;
	private double litbm13Score;
	private double finalScore;
	
	
	public ExtendedStringEntry(StringEntry stringEntry) {
		this.stringEntry = stringEntry;		
	}
	
	
	public ExtendedStringEntry(StringEntry stringEntry, double hi14Score,
			double venekatesanScore, double yu11Score, double litbm13Score, double finalScore) {
		this.stringEntry = stringEntry;
		this.hi14Score = hi14Score;
		this.venekatesanScore = venekatesanScore;
		this.yu11Score = yu11Score;
		this.litbm13Score = litbm13Score;
		this.finalScore = finalScore;
	}
	
	
	public static ExtendedStringEntry parseLine (String line) {
		String [] tokens = line.split(" +");
		
		String protein1 = tokens[0];
		String protein2 = tokens[1];
		double neighborhood = Double.parseDouble(tokens[2]);
		double fusion = Double.parseDouble(tokens[3]);
		double coocurence = Double.parseDouble(tokens[4]);
		double coexpression = Double.parseDouble(tokens[5]);
		double experimental = Double.parseDouble(tokens[6]);
		double database = Double.parseDouble(tokens[7]);
		double textmining = Double.parseDouble(tokens[8]);
		double combinedScore = Double.parseDouble(tokens[9]);
		
		StringEntry se = new StringEntry (protein1, protein2, neighborhood, 
				fusion, coocurence, coexpression, experimental, database, 
				textmining, combinedScore);
		
		double hi14Score = Double.parseDouble(tokens[10]);
		double venekatesanScore = Double.parseDouble(tokens[11]);
		double yu11Score = Double.parseDouble(tokens[12]);
		double litbm13Score = Double.parseDouble(tokens[13]);
		double finalScore = Double.parseDouble(tokens[14]);
		
		return new ExtendedStringEntry(se, hi14Score, venekatesanScore, 
				yu11Score, litbm13Score, finalScore);
	}


	public StringEntry getStringEntry() {
		return stringEntry;
	}


	public double getHi14Score() {
		return hi14Score;
	}


	public double getVenekatesanScore() {
		return venekatesanScore;
	}


	public double getYu11Score() {
		return yu11Score;
	}


	public double getLitbm13Score() {
		return litbm13Score;
	}


	public double getFinalScore() {
		return finalScore;
	}
	
	
	public void setHi14Score(double hi14Score) {
		this.hi14Score = hi14Score;
	}

	public void setVenekatesanScore(double venekatesanScore) {
		this.venekatesanScore = venekatesanScore;
	}

	public void setYu11Score(double yu11Score) {
		this.yu11Score = yu11Score;
	}

	public void setLitbm13Score(double litbm13Score) {
		this.litbm13Score = litbm13Score;
	}

	public void setFinalScore(double finalScore) {
		this.finalScore = finalScore;
	}

	@Override
	public String toString() {
		return String.format("%s %f %f %f %f %f", 
				stringEntry, hi14Score, venekatesanScore, 
				yu11Score, litbm13Score, finalScore);
	}

}
