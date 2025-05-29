"""
Description:
To filter read IDs and it's associated metadata from its paf-file. Optional: Get a .txt file with
just the read IDs (descending order of size, an no duplicates), when filtered across a minimum alignment
length threshold (passed as an optional parameter).

Author: Krishanu Dhar
Date: 10-29-2025 (latest)
"""

import pandas as pd
import argparse
from pathlib import Path

def filter_paf_by_read_ids(read_ids_file, paf_file, output_file, min_alignment, long_ids_file):
    # Load read IDs
    with open(read_ids_file, 'r') as f:
        read_ids = set(line.strip() for line in f if line.strip())

    # Read PAF file
    paf_df = pd.read_csv(paf_file, sep='\t', header=None, engine='python')

    # Filter rows where read ID (column 0) is in read_ids
    filtered_df = paf_df[paf_df[0].isin(read_ids)]

    # Keep only the first 11 columns (0-based index 0-10)
    filtered_df = filtered_df.iloc[:, :11]

    # Sort the read IDs (ascending/descending order of alignment length)
    filtered_df = filtered_df.sort_values(by=10, ascending=False)

    # Save to output file
    filtered_df.to_csv(output_file, sep=' ', header=False, index=False)

    # Sorting out the long aligned read IDs
    if min_alignment and long_ids_file:
        long_alignments = filtered_df[10] >= min_alignment
        long_ids = filtered_df[long_alignments][0].drop_duplicates()
        long_ids.to_csv(long_ids_file, index=False, header=False)

def main():
    parser = argparse.ArgumentParser(description="Filter PAF file by read IDs and extract first 11 columns.")
    parser.add_argument("-r", "--read_ids_file", help="Path to the read IDs text file")
    parser.add_argument("-p", "--paf_file", help="Path to the PAF file")
    parser.add_argument("-o", "--output_file", help="Path to the output file")
    parser.add_argument("-m", "--minimum_alignment", type=int, required=False, default=None, help="Minimum alignment length to extract read IDs")
    parser.add_argument("-oL", "--long_ids_file", type=str, required=False, default=None, help="Path to save read IDs with long alignments")
    args = parser.parse_args()

    filter_paf_by_read_ids(args.read_ids_file, args.paf_file, args.output_file, args.minimum_alignment, args.long_ids_file)


if __name__ == "__main__":
    main()
