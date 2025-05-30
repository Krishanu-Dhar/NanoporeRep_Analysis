#!/bin/bash
#SBATCH --job-name=run_sort_track_length
#SBATCH --cpus-per-task=16
#SBATCH --mem=16G
#SBATCH --time=02:00:00
#SBATCH --partition=serial

python sort_track_length.py \
  --track_file /s/sansam-lab/20250130_NanoporeEduBrduTest/chunk_forksense/track_length/merged_Forks.csv \
  --early_ids /s/sansam-lab/20250130_NanoporeEduBrduTest/chunk_forksense/track_length/replicate_domains/early_reads.csv \
  --late_ids /s/sansam-lab/20250130_NanoporeEduBrduTest/chunk_forksense/track_length/replicate_domains/late_reads.csv \
  --early_output /s/sansam-lab/20250130_NanoporeEduBrduTest/chunk_forksense/track_length/replicate_domains/early_tracks.csv \
  --late_output /s/sansam-lab/20250130_NanoporeEduBrduTest/chunk_forksense/track_length/replicate_domains/late_tracks.csv
