#!/bin/bash
#SBATCH --job-name=run_brdu_edu_sliding
#SBATCH --cpus-per-task=16
#SBATCH --mem=16G
#SBATCH --time=02:00:00
#SBATCH --partition=serial

# This shell script is to run 'brdu_edu_sliding_windows_from_bam.py' on a HPC cluster

# === Loading modules ===
module purge
module load slurm python pandas numpy matplotlib

# === Paths and parameters ===
FILTERED_BED="/path/to/the/filtered_bedfile/final_filtered.bed"
BRDU_PREFIX="/path/to/the/output_directory/with_prefix/BrdU_"
EDU_PREFIX="/path/to/the/output_directory/with_prefix/EdU_"
BAM_FILE="path/to/the/bamfile/sample_15.bam"
WINDOW_SIZE=100 # (in bp, not thymidine positions)
STEP_SIZE=10 # (in bp, not thymidine positions)

# === Run the script ===
python /path/to/the/python_script/brdu_edu_sliding_windows_from_bam.py \
  --bam "$BAM_FILE" \
  --brdu_output "$BRDU_PREFIX" \
  --edu_output "$EDU_PREFIX" \
  --window_bp "$WINDOW_SIZE" \
  --step_size_bp "$STEP_SIZE" \
  --filtered "$FILTERED_BED" \
  --processes 16 \
  --output_per_read
  #--num_reads 2 \ 
  #--write_wig

