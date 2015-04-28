package gene_ontology;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.HashSet;
import java.util.Scanner;

/**
 * Split filtered ontology files to three subontologies 
 * (cellular component - CC, molecular function - MF, biological process - BP)
 * 
 * @author verica
 *
 */
public class GOSubontology {
	// subontologies terms
	private HashSet<String> cc;
	private HashSet<String> mf;
	private HashSet<String> bp;
	
	
	/**
	 * Build three hashsets each with all the terms from one of the
	 * three subontologies. These will be used later on for filtering.
	 * 
	 * @param ccFile
	 * @param mfFile
	 * @param bpFile
	 * @throws FileNotFoundException
	 */
	public GOSubontology (String ccFile, String mfFile, String bpFile) throws FileNotFoundException {
		cc = new HashSet<String>();
		mf = new HashSet<String>();
		bp = new HashSet<String>();		
		String term;
		
		Scanner in = new Scanner(new FileInputStream (ccFile));
		while (in.hasNextLine()) {
			term = in.nextLine().trim();
			cc.add(term);
		}
		in.close();
		
		in = new Scanner(new FileInputStream (mfFile));
		while (in.hasNextLine()) {
			term = in.nextLine().trim();
			mf.add(term);
		}
		in.close();
		
		in = new Scanner(new FileInputStream (bpFile));
		while (in.hasNextLine()) {
			term = in.nextLine().trim();
			bp.add(term);
		}
		in.close();
	}
	
	
	/**
	 * Create three new subontology files from give file
	 * 
	 * @param file: the file that should be split to subontologies
	 * @param subCC: the file that will contain cellular component ontology
	 * @param subMF: the file that will contain molecular function ontology
	 * @param subBP: the file that will contain biological process ontology
	 * @throws IOException
	 */
	public void splitToSubontologies (String file, String subCC, String subMF, 
			                                       String subBP) throws IOException {
		Scanner in = new Scanner (new FileInputStream (file));
		PrintWriter pwcc = new PrintWriter(new FileWriter(subCC));
		PrintWriter pwmf = new PrintWriter(new FileWriter(subMF));
		PrintWriter pwbp = new PrintWriter(new FileWriter(subBP));
		String line;
		String [] tokens;
		
		while (in.hasNextLine()) {
			line = in.nextLine();
			tokens = line.split("\t");
			if (cc.contains(tokens[3])) pwcc.println(line);
			if (mf.contains(tokens[3])) pwmf.println(line);
			if (bp.contains(tokens[3])) pwbp.println(line);
		}
		
		in.close();
		pwcc.close();
		pwmf.close();
		pwbp.close();		
	}

}
