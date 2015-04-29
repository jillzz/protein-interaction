package gene_ontology;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;

public class Main {

	
	public static void main(String[] args) {
		try {
			filtering();
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
				
		try {
			splitting();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
		try {
			irrelevantTermsFiltering();
		} catch (IOException e) {
			e.printStackTrace();
		}
		
	}
	
	
	public static void filtering () throws FileNotFoundException {
		GOFilter f = new GOFilter();
		
		f.filter("data/go/9606_go_knowledge_full.tsv", 
				 "data/human_ppi_data_700", 
				 "data/go/human_ppi700_go.tsv");
		f.filter("data/go/9606_go_knowledge_full.tsv", 
				 "data/human_ppi_data_900", 
				 "data/go/human_ppi900_go.tsv");
		f.filterUnreliable("data/go/human_ppi700_go.tsv", 
				           "data/go/human_ppi700_go_conf.tsv",
				           3);
		f.filterUnreliable("data/go/human_ppi900_go.tsv", 
			               "data/go/human_ppi900_go_conf.tsv",
			               3);		
	}
	
	
	public static void splitting () throws IOException {
		GOSubontology gos = new GOSubontology("data/go/subontologies/CCGOterms.txt", 
					                          "data/go/subontologies/MFGOterms.txt", 
					                          "data/go/subontologies/BPGOterms.txt");
		
		gos.splitToSubontologies("data/go/human_ppi700_go.tsv", 
						         "data/go/split/human_ppi700_go_cc.tsv", 
				                 "data/go/split/human_ppi700_go_mf.tsv", 
				                 "data/go/split/human_ppi700_go_bp.tsv");
		
		gos.splitToSubontologies("data/go/human_ppi700_go_conf.tsv", 
		         				 "data/go/split/human_ppi700_go_cc_conf.tsv", 
                                 "data/go/split/human_ppi700_go_mf_conf.tsv", 
                                 "data/go/split/human_ppi700_go_bp_conf.tsv");
		
		gos.splitToSubontologies("data/go/human_ppi900_go.tsv", 
		                         "data/go/split/human_ppi900_go_cc.tsv", 
                                 "data/go/split/human_ppi900_go_mf.tsv", 
                                 "data/go/split/human_ppi900_go_bp.tsv");
		
		gos.splitToSubontologies("data/go/human_ppi900_go_conf.tsv", 
				 			     "data/go/split/human_ppi900_go_cc_conf.tsv", 
                                 "data/go/split/human_ppi900_go_mf_conf.tsv", 
                                 "data/go/split/human_ppi900_go_bp_conf.tsv");
		
	}
	
	
	public static void irrelevantTermsFiltering () throws IOException {
		RelevantGOTerms t = new RelevantGOTerms ();
		t.findProteinsPerTerm();
		t.buildAnnotationNetwork();
		t.countPoteinsPerTerm();
		t.outputRelevantTerms("data/go/relevant-terms");
			
		File dir = new File("data/go/split");
		File [] filesList = dir.listFiles();
		String outputFile;
		
		for (File file : filesList) {
		    if (file.isFile()) {
		        outputFile = String.format ("%s_clean.tsv", 
							 	file.getCanonicalFile().toString().split("\\.")[0]);
				t.cleanAnnotationFile(file.getCanonicalFile().toString(), 
							          "data/go/relevant-terms", 
							          outputFile);				
		    }
		}
	}
	

}
