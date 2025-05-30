#!/bin/bash
#SBATCH --job-name=run_extract_domain_sorted
#SBATCH --cpus-per-task=16
#SBATCH --mem=16G
#SBATCH --time=02:00:00
#SBATCH --partition=serial

python extract_domain_sorted.py \
	--reads_file /s/sansam-lab/20250130_NanoporeEduBrduTest/chunk_forksense/merged_rightForks.bed \
	--early_file /s/sansam-lab/20250130_NanoporeEduBrduTest/chunk_forksense/track_length/replicate_domains/EarlyRepDomains.bed \
	--late_file /s/sansam-lab/20250130_NanoporeEduBrduTest/chunk_forksense/track_length/replicate_domains/LateRepDomains.bed \
	--early_output /s/sansam-lab/20250130_NanoporeEduBrduTest/chunk_forksense/track_length/replicate_domains/right_early_reads.csv \
	--late_output /s/sansam-lab/20250130_NanoporeEduBrduTest/chunk_forksense/track_length/replicate_domains/right_late_reads.csv \
	--non_overlap_output /s/sansam-lab/20250130_NanoporeEduBrduTest/chunk_forksense/track_length/replicate_domains/right_non_overlapping_reads.csv


