#!/usr/bin/env python
"""
Program for parsing a gtf file to picard/dropseqtools standards
Input: a .gtf standardised using AGAT
Output: a .gtf with added columns "gene ID, transcript ID, gene name, transcript name"
"""

import sys
import argparse
import re

def main():
    """
    main entry point
    This function starts by parsing the command line arguments.
    
    Then it defines regular expressions to be used in the 
    searching for the gene and transcript IDs, as well as the parent,
    if present.

    Then a dictionary called child_parent is created and, opening the input and
    output files, the main loop starts.

    For each line, it skips commented lines (if any) and then splits the line in
    its columns (TAB-separated). It then grabs column 9 and, by creating a tiny
    temporary dictionary, it fills the child_parent dictionary with the gene ID,
    transcript ID, child/parent values, as key/values.

    Then it checks which kind of feature we have at hand, and handles each
    (gene/transcript/exons/other) independently.

    Finally it replaces or adds values to the column 9 and writes it on the
    output file.
    """
    # Parse the command-line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument("input_file", help="path to the input GTF file")
    parser.add_argument("output_file", help="path to the output GTF file")
    args = parser.parse_args()

    # Define regular expressions for matching the columns in column 9
    gene_id_re = re.compile("gene_id=([^;]+)")
    transcript_id_re = re.compile("ID=([^;]+)")
    parent_re = re.compile("Parent=([^;]+)")
    sep_re = re.compile("[^A-Za-z0-9]")

    # Define Child-Parent Dictionary, psst that is a surprise tool that will help us later
    child_parent = {}

    # Open the input and output files
    with open(args.input_file, "r") as f_in, open(args.output_file, "w") as f_out:
        for line in f_in:
            if line.startswith("#"):
                continue
            a = line[-1:]
            if line.endswith(";"):
                line = line[:-1]
            # Split the line into columns
            columns = line.strip().split("\t")
            # Parse the columns in column 9
            col9_fields = columns[8].split(";")
            col9_dict = {}
            if col9_fields[-1:] == [""]:
                col9_fields = col9_fields[:-1]   
            for field in col9_fields:
                key, value = field.strip().split("=", 1) if "=" in field else field.strip().split(" ", 1)
                col9_dict[key] = value.strip('"')
            
            #Fill the dictionary 
            if "Parent" in col9_dict.keys():
                parent_id = col9_dict["Parent"]
                child_id = col9_dict["ID"]
                child_parent[child_id] = parent_id
            
            # If the row corresponds to a gene
            if columns[2] == "gene":
                # Get the gene ID and add it to the column 9 dictionary
                gene_id_match = gene_id_re.search(columns[8])
                if gene_id_match:
                    gene_id = gene_id_match.group(1)
                    col9_dict["gene_name"] = gene_id
            # If the row corresponds to a transcript
            elif columns[2] == "transcript":
                # Get the transcript ID and gene ID and add them to the column 9 dictionary
                transcript_id_match = transcript_id_re.search(columns[8])
                gene_id_match = gene_id_re.search(columns[8])
                if transcript_id_match and gene_id_match:
                    transcript_id = transcript_id_match.group(1)
                    gene_id = gene_id_match.group(1)
                    col9_dict["transcript_id"] = transcript_id
                    col9_dict["gene_name"] = gene_id
                    col9_dict["transcript_name"] = transcript_id
            # If the row corresponds to an exon, CDS, 5" UTR, or 3" UTR
            else:
                # Get the parent ID and add it to the column 9 dictionary
                parent_match = parent_re.search(columns[8])
                if parent_match:
                    parent_id = parent_match.group(1)
                    sep = sep_re.search(parent_id[::-1]).group()
                    # Remove any last termination preceded by a `.`
                    # parent_id = parent_id[::-1].split(sep, 1)[1][::-1] # this was cool but useless
                    col9_dict["gene_id"] = child_parent[parent_match.group(1)]
                    col9_dict["transcript_id"] = parent_match.group(1)
                    col9_dict["gene_name"] = child_parent[parent_match.group(1)]
                    col9_dict["transcript_name"] = parent_match.group(1)
            # Reconstruct the column 9 string
            col9_fields = []
            for key, value in col9_dict.items():
                col9_fields.append('{} "{}"'.format(key, value))
            col9_string = "; ".join(col9_fields)
            # Write the modified line to the output file
            columns[8] = col9_string
            f_out.write("\t".join(columns) + "\n")
    
    return(0)

if __name__ == "__main__":
    """
    Main guard or module guard
    """
    # used to exit the program with the exit code returned by the main function
    sys.exit(main())
    # After runnung the script check in the command line the result: echo $?