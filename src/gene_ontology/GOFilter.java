package gene_ontology;

import graph_building.FileGraphBuilder;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileOutputStream;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.Scanner;

/**
 * Filtering unreliable and unnecessary annotations
 * 
 * @author verica
 *
 */
public class GOFilter {
	
	
	/**
	 * Filter out all the annotations from the gene ontology dataset,
	 * that correspond to proteins that are not present in the
	 * protein interaction dataset
	 * 
	 * @param inputFile: gene ontology file
	 * @param filterFile: protein interaction file
	 * @param outputFile: filtered gene ontology file
	 * @throws FileNotFoundException
	 */
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
	
	
	/**
	 * Filter out unreliable annotations.
	 * As unreliable are considered all annotations with reliability 
	 * score less than the given threshold
	 * 
	 * @param inputFile: annotation file to be filtered
	 * @param outputFile: filtered annotation file
	 * @param threshold: minimum reliability score
	 * @throws FileNotFoundException
	 */
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
