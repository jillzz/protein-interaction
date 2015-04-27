package graph_building;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.HashMap;
import java.util.Scanner;

import cern.colt.matrix.tdouble.impl.SparseCCDoubleMatrix2D;

public class FileGraphBuilder {
	
	public SparseCCDoubleMatrix2D buildGraph (String fileName) throws FileNotFoundException {
		HashMap<String, Integer> proteinToId = readNodes(fileName);
		SparseCCDoubleMatrix2D A = new SparseCCDoubleMatrix2D(proteinToId.size(), proteinToId.size());
		Scanner in = new Scanner(new FileInputStream(fileName));
		String [] tokens;
		
		while (in.hasNextLine()) {
			tokens = in.nextLine().trim().split(" ");
			A.setQuick(proteinToId.get(tokens[0]), 
					   proteinToId.get(tokens[1]), 
					   1);
			A.setQuick(proteinToId.get(tokens[1]), 
					   proteinToId.get(tokens[0]), 
					   1);
		}
		in.close();
				
		return A;
	}
	
	
	public SparseCCDoubleMatrix2D buildWeightedGraph (String fileName) throws FileNotFoundException {
		HashMap<String, Integer> proteinToId = readNodes(fileName);
		SparseCCDoubleMatrix2D A = new SparseCCDoubleMatrix2D(proteinToId.size(), proteinToId.size());
		Scanner in = new Scanner(new FileInputStream(fileName));
		String [] tokens;
		
		while (in.hasNextLine()) {
			tokens = in.nextLine().trim().split(" ");
			A.setQuick(proteinToId.get(tokens[0]), 
					   proteinToId.get(tokens[1]), 
					   Double.parseDouble(tokens[tokens.length-1]));
			A.setQuick(proteinToId.get(tokens[1]), 
					   proteinToId.get(tokens[0]), 
					   Double.parseDouble(tokens[tokens.length-1]));
		}
		in.close();
				
		return A;
	}
	
	public HashMap<String, Integer> readNodes (String filename) throws FileNotFoundException {
		HashMap<String, Integer> proteinToId = new HashMap<String, Integer>();
		String [] tokens;
		int id = 0;
		Scanner in = new Scanner(new FileInputStream(filename));
		
		while (in.hasNextLine()) {
			tokens = in.nextLine().trim().split(" ");
			if (!proteinToId.containsKey(tokens[0]))
				proteinToId.put(tokens[0], id++);
			if (!proteinToId.containsKey(tokens[1]))
				proteinToId.put(tokens[1], id++);
		}				
		in.close();
		
		return proteinToId;
	}

}
