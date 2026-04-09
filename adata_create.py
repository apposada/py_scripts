#!/usr/bin/env python
"""
A python script to create an adata object out of UMI matrix, gene IDs, cell barcodes, and any cell metadata (if provided).
"""
# standard library
import sys # import sys so we can use the exit function
import argparse
# external modules
import anndata
import scipy.sparse as sparse
from scipy.io import mmread
from pandas import read_csv

def main():
    """
    main entry point
    Parses arguments, loads all the required data, prepares the matrix, creates the adata, writes to disk, and exits.
    """
    # part 0: argument parser
    parser=argparse.ArgumentParser(description="Program that makes a h5ad AnnData out of UMI matrix, cell barcodes, gene IDs, and metadata")
    parser.add_argument("-m", help="UMI matrix")
    parser.add_argument("-bc", help="cell barcodes", type = argparse.FileType('r'))
    parser.add_argument("-g", help="gene ids/names", type = argparse.FileType('r'))
    parser.add_argument("-md", help="cell metadata (optional)", type = argparse.FileType('r'))
    parser.add_argument("-o", help="name of h5ad file")
    args = parser.parse_args()

    print("Loading data...")
    # load matrix using scipy sparse
    m = mmread(args.m, spmatrix = True).tocsr().transpose()
    # load cell barcodes
    bcs = []
    for i in args.bc:
        bcs += [i.replace("\n","")]
    # load gene ids
    g = []
    for i in args.g:
        g += [i.replace("\n","")]
    
    print("Making AnnData...")
    # create anndata object
    ad = anndata.AnnData(X = m)
    # label colnames
    ad.obs.index = bcs
    # label rownames
    ad.var.index = g

    # if provided, load metadata and add to anndata object
    if args.md is not None :
        print("Loading cell metadata...")
        md = read_csv(args.md)
        md.index = bcs
        print("Adding cell metadata...")
        ad.obs = md
    
    # write anndata object to disk
    print("Saving...")
    ad.write_h5ad(filename=args.o, compression = "gzip")
    print("Done.")

    return 0 # by convention, return 0 for success, non-zero otherwise


if __name__ == "__main__":
    """
    Main guard or module guard. 
    It prevents code from being executed when the script is imported as a module in another Python script.
    """
    # used to exit the program with the exit code returned by the main function
    sys.exit(main())

    # After runnung the script check in the command line the result: echo $?
