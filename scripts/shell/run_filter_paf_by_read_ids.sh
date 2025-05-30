#!/bin/bash
# This shell script runs a Python script that extracts the metadata associated with a set of read IDs (TXT_FILE), sorts them (based on alignment lengths)
#SBATCH --job-name=run_filter_paf_by_read_ids
#SBATCH --cpus-per-task=16
#SBATCH --mem=16G
#SBATCH --time=02:00:00
#SBATCH --partition=serial

# This shell script runs the script filter_paf_by_read_ids.py

# === Loading modules ===
module purge
module load slurm python pandas numpy matplotlib

# === Paths and parameters ===
TXT_FILE="/s/sansam-lab/rDNA_Rep/align_to_rdna/rdna_read_ids51.sorted.txt"
PAF_FILE="/s/sansam-lab/rDNA_Rep/align_to_rdna/hits_barcode51.paf"
OUTPUT="/s/sansam-lab/rDNA_Rep/align_to_rdna/Paf_hits/Paf_hits_barcode51.txt"
LONG_READS="/s/sansam-lab/rDNA_Rep/align_to_rdna/Paf_hits/long_hits_barcode51_10K.txt"
MIN_ALIGN=10000

# === Run the script ===
python3 /s/sansam-lab/rDNA_Rep/align_to_rdna/filter_paf_by_read_ids.py \
  -r "$TXT_FILE" \
  -p "$PAF_FILE" \
  -o "$OUTPUT" \
  -m "$MIN_ALIGN" \
  -oL "$LONG_READS"

# === Counting the number of reads that are above the minimum alignment length ===
wc -l /s/sansam-lab/rDNA_Rep/align_to_rdna/Paf_hits/long_hits_barcode51_10K.txt
# === Printing on run completion === #
echo Successfully Ran
