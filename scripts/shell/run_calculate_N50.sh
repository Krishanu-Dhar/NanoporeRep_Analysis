#!/bin/bash
#SBATCH --job-name=run_calculate_N50
#SBATCH --time=01:00:00

# This shell script is to run the calculate_N50 python script in a HPC

# ===Loading modules=== 
module purge
module load python samtools matplotlib

# Parent directory where you want all the PNGs to go
PARENT_DIR=/path/to/output_directory/plots

# Ensure pysam is in your environment
python /path/to/directory/which_has_the/python_script/calculate_N50.py --outdir $PARENT_DIR \
/path/to/directory/which/has_the_bamfiles/*.bam
