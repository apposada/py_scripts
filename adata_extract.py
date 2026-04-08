#!/usr/bin/env python
"""
A python script to extract UMI matrix, cell metadata, and feature name(s) (plus metadata optionally)
This script opens scanpy h5ad objects and does exactly what it sais on the tin.
"""

import sys # import sys so we can use the exit function
import argparse
import scanpy as sc
import numpy as np
import anndata
import gzip
from scipy.io import mmwrite

def main():
    """
    main entry point
    This is where the core of what is done happens
    """
    # Parsing arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("filename")
    args = parser.parse_args()

    filename = args.filename
    basename = filename.replace(".h5ad","")

    outname_bcs = basename + ".bcs.csv"
    outname_cellinfo = basename + ".cellinfo.csv"
    outname_features = basename + ".features.csv"
    outname_umimatrix = basename + ".UMImatrix.mtx.gz"

    # Load the adata file
    adata = sc.read_h5ad(filename)

    # Extract cell IDs
    cell_names = adata.obs.index.tolist()

    with open(outname_bcs, "w") as cell_ids_outfile:
        cell_ids_outfile.write("\n".join(str(i) for i in cell_names))

    # Extract cell metadata
    adata.obs.to_csv(outname_cellinfo)

    # Extract feature names
    gene_names = adata.var.index.tolist()

    with open(outname_features, "w") as gene_names_outfile:
        gene_names_outfile.write("\n".join(str(i) for i in gene_names))


    if adata.raw != None :
        # Get the raw counts matrix
        umimatrix = adata.raw.X
    else:
        umimatrix = adata.X.astype(int)

    # Save the raw counts matrix as .mtx.gz
    with gzip.open(outname_umimatrix, "wb") as f:
        mmwrite(f, umimatrix)

    return 0 # by convention, return 0 for success, non-zero otherwise

if __name__ == "__main__":
    """
    Main guard or module guard. 
    It prevents code from being executed when the script is imported as a module in another Python script.
    """
    # used to exit the program with the exit code returned by the main function
    sys.exit(main())
    # After running the script check in the command line the result: echo $?
