package gene_ontology;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Scanner;

/**
 * Filter out gene annotation (GO terms) that are irrelevant (uninformative).
 * A term is considered relevant if it's used for annotation of al least 30
 * proteins and all it's children terms are used for annotation of less 
 * than 30 proteins each.
 * 
 * @author verica
 *
 */
public class RelevantGOTerms {
	
	private HashMap<String, HashSet<String>> termToProteins;      // Every ontology term is mapped to a set of proteins it annotates
	                                                              //    (proteins annotated by children excluded)
	private HashMap<String, HashSet<String>> annotationTree;      // Every term is mapped to a set of children terms
	private HashMap<String, Integer> termToCount;                 // Every term is mapped to number of proteins annotated 
																  //    (proteins annotated by it's children included)
	
	private static final String ONTOLOGY_FILE = "data/go/9606_go_knowledge_full.tsv";
	// subontologies relation files
	private static final String CC_RELATIONS= "data/go/subontologies/CCGOfull.txt";
	private static final String MF_RELATIONS= "data/go/subontologies/MFGOfull.txt";
	private static final String BP_RELATIONS= "data/go/subontologies/BPGOfull.txt";
	private static final int ANNOTATION_THRESHOLD = 30;           // annotation threshold for filtering out irrelevant terms
	
	
	public RelevantGOTerms () {
		this.termToProteins = new HashMap<String, HashSet<String>>();
		this.annotationTree = new HashMap<String, HashSet<String>>();
		this.termToCount = new HashMap<String, Integer>();
	}
	
	
	/**
	 * Counts proteins annotated per term
	 * 
	 * @throws FileNotFoundException
	 */
	public void findProteinsPerTerm () throws FileNotFoundException {
		Scanner in = new Scanner(new FileInputStream (ONTOLOGY_FILE));
		String [] tokens;
		String protein, ontology;
				
		while (in.hasNextLine()) {
			tokens = in.nextLine().trim().split("\t");
			protein = tokens[1];
			ontology = tokens[3];
			if (!termToProteins.containsKey(ontology))
				termToProteins.put(ontology, new HashSet<String>());
			termToProteins.get(ontology).add(protein);
		}
		in.close();
	}
	
	
	/**
	 * Finds the number of proteins each term annotates,
	 * proteins annotated by it's children inclusive 
	 */
	public void countPoteinsPerTerm () {
		for (String term : termToProteins.keySet())
			termToCount.put(term, countProteinsHierarchically(term));
	}
	
	
	/**
	 * Return the number of proteins the given term annotates
	 * counting also proteins annotated by their children terms
	 * 
	 * @param term
	 * @return
	 */
	private int countProteinsHierarchically (String term) {
		if (!termToProteins.containsKey(term)) return 0;
		
		int count = termToProteins.get(term).size();
		if (annotationTree.containsKey(term))
			for (String childTerm : annotationTree.get(term))
				count += countProteinsHierarchically(childTerm);
		
		return count;
	}
	
	
	/**
	 * Build parent-child GO annotation network
	 * 
	 * @throws FileNotFoundException
	 */
	public void buildAnnotationNetwork () throws FileNotFoundException {
		String [] tokens;
		String parent, child;
		
		Scanner in = new Scanner(new FileInputStream(CC_RELATIONS));
		while (in.hasNextLine()) {
			tokens = in.nextLine().trim().split(" ");
			if (tokens[1].equals("is_a") || tokens[1].equals("part_of")) {
				parent = tokens[2];
				child = tokens[0];
				if (!annotationTree.containsKey(parent))
					annotationTree.put(parent, new HashSet<String>());
				annotationTree.get(parent).add(child);
			}
		}
		in.close();
		
		in = new Scanner(new FileInputStream(MF_RELATIONS));
		while (in.hasNextLine()) {
			tokens = in.nextLine().trim().split(" ");
			if (tokens[1].equals("is_a") || tokens[1].equals("part_of")) {
				parent = tokens[2];
				child = tokens[0];
				if (!annotationTree.containsKey(parent))
					annotationTree.put(parent, new HashSet<String>());
				annotationTree.get(parent).add(child);
			}
		}
		in.close();
		
		in = new Scanner(new FileInputStream(BP_RELATIONS));
		while (in.hasNextLine()) {
			tokens = in.nextLine().trim().split(" ");
			if (tokens[1].equals("is_a") || tokens[1].equals("part_of")) {
				parent = tokens[2];
				child = tokens[0];
				if (!annotationTree.containsKey(parent))
					annotationTree.put(parent, new HashSet<String>());
				annotationTree.get(parent).add(child);
			}
		}
		in.close();		
	}
	
	
	/**
	 * Output all relevant terms to a file
	 * 
	 * @param outputFile
	 * @throws IOException
	 */
	public void outputRelevantTerms (String outputFile) throws IOException {
		PrintWriter pw = new PrintWriter (new FileWriter (outputFile));
		
		for (String term : termToCount.keySet())
			if (isRelevant(term))
				pw.println(term);
		
		pw.close();
	}
	
	
	/**
	 * Check if given term is relevant.
	 * A term is considered relevant if it annotates at least threshold proteins,
	 * but all their children annotate less than threshold proteins each.
	 * 
	 * @param term
	 * @return
	 */
	public boolean isRelevant (String term) {
		if (termToCount.get(term) < ANNOTATION_THRESHOLD) return false;
		
		if (annotationTree.containsKey(term)) 
			for (String childTerm : annotationTree.get(term))
				if (termToCount.containsKey(childTerm) && termToCount.get(childTerm) >= ANNOTATION_THRESHOLD)
					return false;
		
		return true;
	}
	
	
	/**
	 * Clean given annotation file from all uninformative (irelevant) annotations
	 * 
	 * @param annotationFile: the file to be cleaned
	 * @param relevantTermsFile: file that lists all relevant terms
	 * @param outputFile: cleaned output file
	 * @throws IOException
	 */
	public void cleanAnnotationFile (String annotationFile, String relevantTermsFile, 
			                         String outputFile) throws IOException {
		HashSet<String> relevantTerms = new HashSet<String>();
		String line;
				
		Scanner in = new Scanner (new FileInputStream (relevantTermsFile));
		while (in.hasNextLine())
			relevantTerms.add(in.nextLine().trim());
		in.close();
		
		in = new Scanner (new FileInputStream (annotationFile));
		PrintWriter pw = new PrintWriter (new FileWriter (outputFile));
		while (in.hasNextLine()) {
			line = in.nextLine();
			if (relevantTerms.contains(line.split("\t")[3]))
				pw.println(line);
		}
		in.close();
		pw.close();
	}

}