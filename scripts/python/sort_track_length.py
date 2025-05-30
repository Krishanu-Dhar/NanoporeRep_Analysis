import pandas as pd
import argparse

parser = argparse.ArgumentParser(description="Extract track lengths for early and late replication reads.")
parser.add_argument("--track_file", required=True, help="CSV file with all read IDs and track lengths")
parser.add_argument("--early_ids", required=True, help="CSV from previous step containing early replication read IDs")
parser.add_argument("--late_ids", required=True, help="CSV from previous step containing late replication read IDs")
parser.add_argument("--early_output", required=True, help="Output CSV for early replication track lengths")
parser.add_argument("--late_output", required=True, help="Output CSV for late replication track lengths")
args = parser.parse_args()

# Load full track dataset
track_df = pd.read_csv(args.track_file)

# Load read IDs that belong to early and late domains
early_df = pd.read_csv(args.early_ids)
late_df = pd.read_csv(args.late_ids)

# Filter by matching read_ids
early_reads = track_df[track_df["read_id"].isin(early_df["read_id"])]
late_reads = track_df[track_df["read_id"].isin(late_df["read_id"])]

# Save outputs
early_reads.to_csv(args.early_output, index=False)
late_reads.to_csv(args.late_output, index=False)

# Report counts
print(f"Early replication reads with track data: {len(early_reads)}")
print(f"Late replication reads with track data: {len(late_reads)}")
