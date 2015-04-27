package gene_ontology;

import graph_building.FileGraphBuilder;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.Scanner;

public class GOFilter {
	
	public void filter (String inputFile, String filterFile, String outputFile) 
			throws FileNotFoundException {
		Scanner in = new Scanner (new FileInputStream(inputFile));
		PrintWriter out = new PrintWriter(new FileOutputStream(outputFile));
		FileGraphBuilder tmp = new FileGraphBuilder();
		HashMap<String, Integer> proteinToId = tmp.readNodes(filterFile);
		
		String line;
		String [] tokens;	
		while (in.hasNextLine()) {
			line = in.nextLine().trim();
			tokens = line.split("\t");
			if (proteinToId.containsKey("9606." + tokens[1]))
				out.println(line);
		}
				
		out.close();
		in.close();
	} 
	
	
	public void filterUnreliable (String inputFile, String outputFile, int threshold) 
			throws FileNotFoundException {
		Scanner in = new Scanner (new FileInputStream(inputFile));
		PrintWriter out = new PrintWriter(new FileOutputStream(outputFile));
		String line;
		String [] tokens;	
		int trust;
		while (in.hasNextLine()) {
			line = in.nextLine().trim();
			tokens = line.split("\t");
			trust = Integer.parseInt(tokens[tokens.length - 1]);
			if (trust >= threshold)
				out.println(line);
		}
				
		out.close();
		in.close();
	}

}
