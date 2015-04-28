package gene_ontology;

import java.io.FileInputStream;
import java.io.FileNotFoundException;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Scanner;

/**
 * Filter out gene annotation (GO terms) that are irrelevant (uninformative).
 * A term is considered relevant if it's used for annotation of al least 30
 * proteins and all it's children terms are used for annotation of less 
 * than 30 proteins.
 * 
 * @author verica
 *
 */
public class RelevantGOTerms {
	
	public static void main(String[] args) {
		RelevantGOTerms t = new RelevantGOTerms ();
		try {
			t.findProteinsPerTerm();
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		
		int count = 0;
		System.out.println(t.termToProteins.size());
		for (String key : t.termToProteins.keySet()) {
			if (count > 10) break;
			System.out.println(key + ":\t" + t.termToProteins.get(key).size());
		}

	}
	
	// Every ontology term is mapped to a set of proteins it annotates
	private HashMap<String, HashSet<String>> termToProteins;
	private static final String ONTOLOGY_FILE = "data/go/9606_go_knowledge_full.tsv";
	
	
	public RelevantGOTerms () {
		this.termToProteins = new HashMap<String, HashSet<String>>();
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
	
	

}
