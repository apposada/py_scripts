#!/usr/bin/env python
"""
python boilerplate for scripts
describe the program here
"""

import sys # import sys so we can use the exit function
import argparse
import math
import re

def main():
    """
    main entry point
    All functions should have a docstring
    """
    # part 0: argument parser
    parser=argparse.ArgumentParser(description="Program that makes a lookup table of seqIDs")
    parser.add_argument("-i", help="Input FASTA file") # , type = argparse.FileType('r'))
    parser.add_argument("-o", help="output filename. Lookup table with replacement header lines, column 1: original, column 2: replacement")
    parser.add_argument("-name", help="Name template for sequences")
    args = parser.parse_args()

    # Check if -name does not exist, then infer from .fa
    if args.name is not None :
        sp = args.name
    else :
        path_re = re.compile("^.*/")
        basename_re = re.compile(".[^\\.]+$") # should be a regex of anything after the LAST dot
        cleanpath = re.sub(path_re, "", args.i)
        basename = re.sub(basename_re, "", cleanpath) 
        sp = basename
    
    # count number of lines, num digits etc.
    counter = 0
    oldIDs = list()
    f = open(args.i, "r")
    for line in f:
        if line.startswith(">"):
            oldIDs += [line.replace("\n","")]
            counter += 1
    ndigits = int(math.log(counter, 10))+1

    newIDs = [f">{sp}_{i:0{ndigits}}" for i in range(1,(counter+1))]

    outputfile = open(args.o,'w')

    for i,j in zip(oldIDs,newIDs):
        a = [i,j]
        outputfile.write("\t".join(a)+"\n")

    return 0 # by convention, return 0 for success, non-zero otherwise


if __name__ == "__main__":
    """
    Main guard or module guard. 
    It prevents code from being executed when the script is imported as a module in another Python script.
    """
    # used to exit the program with the exit code returned by the main function
    sys.exit(main())
    # After runnung the script check in the command line the result: echo $?
