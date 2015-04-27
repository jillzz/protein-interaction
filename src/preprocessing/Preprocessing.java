package preprocessing;


import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Scanner;


public class Preprocessing {
	private static final double HI14_VALUE = 0.95;
	private static final double VENEKATESAN_VALUE = 0.85;
	private static final double YU11_VALUE = 0.85;
	private static final double LITBM13_VALUE = 0.90;
	
	private String stringData;
	private String stringToEntrez;
	private String hi14;
	private String venekatesan;
	private String yu11;
	private String litbm13;
		
	private String output;
	
	private ArrayList<StringEntry> stringList;
	private HashMap<String, Integer> entrezMap;
	private HashSet<String> hi14Pair;
	private HashSet<String> venekatesanPair;
	private HashSet<String> yu11Pair;
	private HashSet<String> litbm13Pair;
	
	private ArrayList<ExtendedStringEntry> extStringList;	

	
	public Preprocessing(String stringData, String stringToEntrez, String hi14,
			String venekatesan, String yu11, String litbm13, String output) throws FileNotFoundException {
		this.stringData = stringData;
		this.stringToEntrez = stringToEntrez;
		this.hi14 = hi14;
		this.venekatesan = venekatesan;
		this.yu11 = yu11;
		this.litbm13 = litbm13;
		this.output = output;
		
		this.stringList = new ArrayList<StringEntry>();
		this.entrezMap = new HashMap<String, Integer>();
		this.hi14Pair = new HashSet<String>();
		this.venekatesanPair = new HashSet<String>();
		this.yu11Pair = new HashSet<String>();
		this.litbm13Pair = new HashSet<String>();
		this.extStringList = new ArrayList<ExtendedStringEntry>();
		
		readStringData();
		readMappings();
		readHi14Data();
		readVenekatesanData();
		readYu11Data();
		readLitbm13Data();
	}

	
	private void readStringData () throws FileNotFoundException {
		Scanner in = new Scanner(new FileInputStream(stringData));
		in.nextLine();
		while (in.hasNextLine()) 
			stringList.add(StringEntry.parseLine(in.nextLine().trim()));
		in.close();
		
		System.out.println("String data read-in");
	}
	
	
	private void readMappings () throws FileNotFoundException {
		Scanner in = new Scanner(new FileInputStream(stringToEntrez));
		in.nextLine();
		String [] tokens;
		while (in.hasNextLine()) {
			tokens = in.nextLine().trim().split("\t");
			entrezMap.put(tokens[1], Integer.parseInt(tokens[0]));
		}
		in.close();
		
		System.out.println("Mappings read-in");
	}
	
	
	private void readHi14Data () throws FileNotFoundException {
		Scanner in = new Scanner(new FileInputStream(hi14));
		in.nextLine();
		String [] tokens;
		while (in.hasNextLine()) {
			tokens = in.nextLine().trim().split("\t");
			hi14Pair.add(String.format("%s %s", tokens[0], tokens[2]));
		}
		in.close();
		
		System.out.println("Hi14 data read-in");
	}
	
	
	private void readVenekatesanData () throws FileNotFoundException {
		Scanner in = new Scanner(new FileInputStream(venekatesan));
		in.nextLine();
		String [] tokens;
		while (in.hasNextLine()) {
			tokens = in.nextLine().trim().split("\t");
			venekatesanPair.add(String.format("%s %s", tokens[0], tokens[3]));
		}
		in.close();
		
		System.out.println("Venekatesan data read-in");
	}
	
	
	private void readYu11Data () throws FileNotFoundException {
		Scanner in = new Scanner(new FileInputStream(yu11));
		in.nextLine();
		String [] tokens;
		while (in.hasNextLine()) {
			tokens = in.nextLine().trim().split("\t");
			yu11Pair.add(String.format("%s %s", tokens[0], tokens[2]));
		}
		in.close();
		
		System.out.println("Yu11 data read-in");
	}
	
	
	private void readLitbm13Data () throws FileNotFoundException {
		Scanner in = new Scanner(new FileInputStream(litbm13));
		in.nextLine();
		String [] tokens;
		while (in.hasNextLine()) {
			tokens = in.nextLine().trim().split("\t");
			litbm13Pair.add(String.format("%s %s", tokens[0], tokens[2]));
		}
		in.close();
		
		System.out.println("LitBM13 data read-in");
	}

	
	public void buildCombinedData () {
		String pair1, pair2;
		double hi14Score, venekatesanScore, yu11Score, litbm13Score, finalScore;
		for (int i = 0; i < stringList.size(); i++) {
			pair1 = String.format("%d %d", 
					entrezMap.get(stringList.get(i).getProtein1()), 
					entrezMap.get(stringList.get(i).getProtein2()));
			pair2 = String.format("%d %d", 
					entrezMap.get(stringList.get(i).getProtein2()), 
					entrezMap.get(stringList.get(i).getProtein1()));
						
			if (hi14Pair.contains(pair1) || hi14Pair.contains(pair2))
				hi14Score = HI14_VALUE;
			else hi14Score = 0;
			
			if (venekatesanPair.contains(pair1) || venekatesanPair.contains(pair2))
				venekatesanScore = VENEKATESAN_VALUE;
			else venekatesanScore = 0;
			
			if (yu11Pair.contains(pair1) || yu11Pair.contains(pair2))
				yu11Score = YU11_VALUE;
			else yu11Score = 0;
			
			if (litbm13Pair.contains(pair1) || litbm13Pair.contains(pair2))
				litbm13Score = LITBM13_VALUE;
			else litbm13Score = 0;
			
			finalScore = 1 - ((1 - stringList.get(i).getCombinedScore() / 1000.0) *
					          (1 - hi14Score) * (1 - venekatesanScore) * 
					          (1 - yu11Score) * (1 - litbm13Score));
			
			extStringList.add(new ExtendedStringEntry(stringList.get(i), 
					                                  hi14Score * 1000, 
					                                  venekatesanScore * 1000, 
					                                  yu11Score * 1000, 
					                                  litbm13Score * 1000, 
					                                  finalScore * 1000));
		}
		
		System.out.println("Combined data built");
	}
	
	
	public void outputCombinedData () throws IOException  {
		PrintWriter out = new PrintWriter (
				new FileWriter (output));
		for (int i = 0; i < extStringList.size(); i++) 
			out.println(extStringList.get(i));
		
		out.close();
		
		System.out.println("Output finished");
	}
	
	
	public void outputbyScore (double minScore) throws IOException  {
		PrintWriter out = new PrintWriter (
				new FileWriter (String.format("data/human_ppi_data_%d", (int) minScore)));
		for (int i = 0; i < extStringList.size(); i++)
			if (extStringList.get(i).getFinalScore() >= minScore)
				out.println(extStringList.get(i));
		
		out.close();
		
		System.out.println("Minimum score output finished");
	}

}
