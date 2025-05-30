# Nanopore Replication Analysis

This repository contains Python and shell scripts for performing downstream analysis of EdU and BrdU tracks from Nanopore sequencing data. Downstream analysis includes data parsing, read filtering, replication track visualization, etc.

## Structure

- `scripts/python/`: Python scripts for data parsing, filtering, and visualization
- `scripts/shell/`: Shell scripts for independent HPC cluster jobs and to run the corresponding Python scripts
- `data/`: Raw input files (not tracked)
- `results/`: Output files (not tracked)
- `logs/`: Log files from pipeline execution

## Usage

Scripts can be run individually on pre-processed sequencing data, or as a part/downstream of a Snakemake pipeline (see [`SansamLab-Pipelines-Genomics/ReplisomeTracer`] (https://github.com/SansamLab-Pipelines-Genomics/ReplisomeTracer)).

## Workflow


## Author
Krishanu Dhar
