package preprocessing;

public class StringEntry {
	private String protein1;
	private String protein2;
	private double neighborhood;
	private double fusion;
	private double coocurence;
	private double coexpression;
	private double experimental;
	private double database;
	private double textmining;
	private double combinedScore;
	
	
	public StringEntry(String protein1, String protein2, double neighborhood,
			double fusion, double coocurence, double coexpression,
			double experimental, double database, double textmining,
			double combinedScore) {
		this.protein1 = protein1;
		this.protein2 = protein2;
		this.neighborhood = neighborhood;
		this.fusion = fusion;
		this.coocurence = coocurence;
		this.coexpression = coexpression;
		this.experimental = experimental;
		this.database = database;
		this.textmining = textmining;
		this.combinedScore = combinedScore;
	}


	public static StringEntry parseLine (String line) {
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
		
		return new StringEntry(protein1, protein2, neighborhood, 
				fusion, coocurence, coexpression, experimental, 
				database, textmining, combinedScore);
	}


	public String getProtein1() {
		return protein1;
	}


	public String getProtein2() {
		return protein2;
	}


	public double getNeighborhood() {
		return neighborhood;
	}


	public double getFusion() {
		return fusion;
	}


	public double getCoocurence() {
		return coocurence;
	}


	public double getCoexpression() {
		return coexpression;
	}


	public double getExperimental() {
		return experimental;
	}


	public double getDatabase() {
		return database;
	}


	public double getTextmining() {
		return textmining;
	}


	public double getCombinedScore() {
		return combinedScore;
	}	
	
	@Override
	public String toString() {
		return String.format("%s %s %f %f %f %f %f %f %f %f",
				protein1, protein2, neighborhood, fusion, coocurence, 
				coexpression, experimental, database, textmining, combinedScore);
	}
}
