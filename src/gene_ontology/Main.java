package gene_ontology;

import java.io.FileNotFoundException;

public class Main {

	public static void main(String[] args) {
		GOFilter f = new GOFilter();
		
		try {
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
		} catch (FileNotFoundException e) {
			e.printStackTrace();
		}
	}

}
