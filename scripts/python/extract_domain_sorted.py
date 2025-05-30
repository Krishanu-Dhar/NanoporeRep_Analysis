"""
Script Name: extract_domain_sorted.py

Description:
This Python script extracts early v/s late read IDs and their chromosome number, start and end genomic
positions, start and end of the domain (early/late) it was found in. 

Arguments:
--reads_file: Path to a BED file that has replication fork read IDs and metadata from forkSense
--early_file: Path to a BED file that has genomics domains assigned to early replicating regions in the human genome
--late_file:  Path to a BED file that has genomics domains assigned to late replicating regions in the human genome
--early_output: CSV output file and path that has read IDs and few of the metadata of early replicating (Will update to include the important ones only)
--late_output: CSV output file and path that has read IDs and few of the metadata of late replicating (Will update to include the important ones only)
--non_overlap_output: CSV output file and path that has read IDs and few of the metadata of reads that don't overlap in either
"""
import pandas as pd
import argparse


def load_bed_file(filepath, is_domain_file=False):
    """
    Load a BED file.
    If it's a domain file (early/late replication domains), rename columns accordingly.
    Otherwise, load Nanopore reads and extract relevant columns.
    """
    if is_domain_file:
        df = pd.read_csv(filepath, sep=r"\s+", header=None)
        df.columns = ["chrom", "start_domain", "end_domain"]
    else:
        df = pd.read_csv(filepath, sep=r"\s+", header=None)
        df.columns = ["chrom", "start", "end", "read_id"] + list(range(4, df.shape[1]))
        df = df[["chrom", "start", "end", "read_id"]]  # Keep relevant columns only
    return df


def find_overlapping_reads(reads_df, domains_df):
    """
    Perform an interval overlap between reads and replication domains.
    Keeps only the reads that overlap with a domain on the same chromosome.
    """
    merged = pd.merge(reads_df, domains_df, on="chrom")
    overlaps = merged[(merged["start"] < merged["end_domain"]) & (merged["end"] > merged["start_domain"])]
    return overlaps


def main(args):
    # Load input BED files
    reads = load_bed_file(args.reads_file)
    early_domains = load_bed_file(args.early_file, is_domain_file=True)
    late_domains = load_bed_file(args.late_file, is_domain_file=True)

    # Find overlapping reads for early and late replication domains
    early_overlaps = find_overlapping_reads(reads, early_domains)
    late_overlaps = find_overlapping_reads(reads, late_domains)

    # Sort results by read_id for consistency
    early_overlaps = early_overlaps.sort_values(by=["read_id"])
    late_overlaps = late_overlaps.sort_values(by=["read_id"])

    # Identify read IDs that do not overlap with either domain
    early_read_ids = set(early_overlaps["read_id"])
    late_read_ids = set(late_overlaps["read_id"])
    all_overlap_ids = early_read_ids.union(late_read_ids)
    non_overlap_reads = reads[~reads["read_id"].isin(all_overlap_ids)]

    # Write results to CSV files
    early_overlaps.to_csv(args.early_output, index=False)
    late_overlaps.to_csv(args.late_output, index=False)
    if args.non_overlap_output:
        non_overlap_reads.to_csv(args.non_overlap_output, index=False)

    # Print summary statistics
    print(f"Total reads in early replicating domains: {len(early_read_ids)}")
    print(f"Total reads in late replicating domains: {len(late_read_ids)}")
    print(f"Total reads not in early or late domains: {non_overlap_reads['read_id'].nunique()}")


if __name__ == "__main__":
    # Set up argument parser to allow command-line usage
    parser = argparse.ArgumentParser(description="Extract and sort read IDs overlapping replication domains.")
    parser.add_argument("--reads_file", required=True, help="Path to the BED file of Nanopore reads.")
    parser.add_argument("--early_file", required=True, help="Path to the BED file of early replication domains.")
    parser.add_argument("--late_file", required=True, help="Path to the BED file of late replication domains.")
    parser.add_argument("--early_output", required=True, help="CSV output path for early domain overlapping reads.")
    parser.add_argument("--late_output", required=True, help="CSV output path for late domain overlapping reads.")
    parser.add_argument("--non_overlap_output", help="CSV output path for reads not overlapping any domain.")

    args = parser.parse_args()
    main(args)
