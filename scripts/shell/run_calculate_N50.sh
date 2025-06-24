#!/bin/bash
#SBATCH --job-name=run_calculate_N50
#SBATCH --time=01:00:00

# This shell script is to run the calculate_N50 python script in a HPC

# ===Loading modules=== 
module purge
module load python samtools matplotlib

# Parent directory where you want all the PNGs to go
PARENT_DIR=/s/sansam-lab/Multi_Label/ReplisomeTracer/plot_outputs

# Ensure pysam is in your environment
python /s/sansam-lab/Multi_Label/ReplisomeTracer/scripts/calculate_N50.py --outdir $PARENT_DIR \
/s/sansam-lab/Multi_Label/ReplisomeTracer/DNAscent_Snakemake/results/demuxed/*.bam
