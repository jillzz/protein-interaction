package graph_building;

import java.io.FileNotFoundException;

import cern.colt.matrix.tdouble.impl.SparseCCDoubleMatrix2D;

public class Main {

	public static void main(String[] args) {
		FileGraphBuilder fgb = new FileGraphBuilder();
		SparseCCDoubleMatrix2D A700 = null, A900 = null;
		try {
			A700 = fgb.buildWeightedGraph("data/human_ppi_data_700");
			A900 = fgb.buildWeightedGraph("data/human_ppi_data_900");
		} catch (FileNotFoundException e) {
			e.printStackTrace();
			System.exit(-1);
		}
		
		System.out.println("A700 size: " + A700.columns());
		System.out.println("A900 size: " + A900.columns());
		
	}

}
