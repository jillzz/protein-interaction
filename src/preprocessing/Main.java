package preprocessing;

import java.io.FileNotFoundException;
import java.io.IOException;

public class Main {

	public static void main(String[] args) {
		Preprocessing preprocessor = null;
		try {
			preprocessor = new Preprocessing(
					"data/string/9606.protein.links.detailed.v9.1.txt", 
					"data/mappings/entrez_gene_id.vs.string.v9.05.28122012.txt", 
					"data/ccsb/HI-II-14.tsv", 
					"data/ccsb/Venkatesan-09.tsv", 
					"data/ccsb/Yu-11.tsv", 
					"data/ccsb/Lit-BM-13.tsv", 
					"data/human_ppi_data");
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
		
		preprocessor.buildCombinedData();
		/*
		try {
			preprocessor.outputCombinedData();
		} catch (IOException e) {
			e.printStackTrace();
		}
		*/
		try {
			preprocessor.outputbyScore(700);
			preprocessor.outputbyScore(900);
		} catch (IOException e) {
			e.printStackTrace();
		}
	}

}
