#!/usr/bin/env python
"""
Copied from  BrissMiller's answer at biostars: https://www.biostars.org/p/103089/#441715

Replace specific headers from a fa file using a custom made lookup table, tab delimited.
Use grep "^>" fasta.fa to help generate that lookup table.
Code based off of solution from replace fasta headers with another name in a text file

Example lookup table line:
>old_line  >new_linegrep
"""

import sys # import sys so we can use the exit function
import argparse
import csv

def main():
    """
    main entry point
    This is where the core of what is done happens
    """
    # part 0: argument parser
    parser=argparse.ArgumentParser(description="Program that replaces fasta headers")
    parser.add_argument("-i", help="Input FASTA file", type = argparse.FileType('r'))
    parser.add_argument("-l", help="Lookup table with replacement header lines, column 1: original, column 2: replacement")
    parser.add_argument("-o", help="Output FASTA file name")
    args = parser.parse_args()

    # part 1: create dictionary
    lookup_dict = {}
    with open(args.l) as lookup_handle:
        lookup_list = csv.reader(lookup_handle, delimiter='\t')
        for entry in lookup_list:
            lookup_dict[entry[0].replace(">","")] = entry[1].replace(">","")

    # part 2
    # create an output file
    newfasta=open(args.o,'w')
    # read in the fa line by line and replace the header if it is in the lookup table
    for line in args.i:
        line = line.rstrip("\n")
        if line.startswith('>'):
            seqid = str(line).replace(">","")
            if seqid in lookup_dict.keys():
                newname = '>'+lookup_dict[seqid]
                newfasta.write(newname+"\n")
            else:
                newfasta.write(line+"\n")
        else:
            newfasta.write(line+"\n")

    return 0 # by convention, return 0 for success, non-zero otherwise

if __name__ == "__main__":
    """
    Main guard or module guard.
    It prevents code from being executed when the script is imported as a module in another Python script.
    """
    # used to exit the program with the exit code returned by the main function
    sys.exit(main())
    # After running the script check in the command line the result: echo $?
