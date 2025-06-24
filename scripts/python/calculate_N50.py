#!/usr/bin/env python3
"""
calculate_N50.py: Calculate N50 and generate read-length histograms and ECDF plots for one or more BAM files.

Usage:
    python calculate_N50.py --outdir /path/to/parent BAM1.bam BAM2.bam ...

This script:
  - Extracts read lengths from each BAM (primary, mapped reads only).
  - Computes N50, mean, median, and total read count per sample.
  - Generates individual-sample histograms and ECDF plots.
  - Generates overlayed histograms and ECDFs across all samples.
  - Writes all output PNGs into a subdirectory named 'n50_outputs' under the provided parent directory.
"""

import argparse
import os
import sys
import pysam
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import statistics as stat


def get_read_lengths(bam_path):
    """Extract read lengths from a BAM file (primary, mapped reads only)."""
    try:
        bam = pysam.AlignmentFile(bam_path, "rb")
    except Exception as e:
        raise RuntimeError(f"Could not open BAM '{bam_path}': {e}")
    lengths = []
    for read in bam:
        if read.is_secondary or read.is_supplementary or read.is_unmapped:
            continue
        qlen = read.query_length
        if qlen is not None:
            lengths.append(qlen)
    bam.close()
    if not lengths:
        raise RuntimeError(f"No valid reads in '{bam_path}'")
    return lengths


def compute_stats(lengths):
    """Compute N50, mean, median, and count from a list of lengths."""
    sorted_desc = sorted(lengths, reverse=True)
    total_bases = sum(sorted_desc)
    half = total_bases / 2.0
    cum = 0
    n50 = sorted_desc[-1]
    for L in sorted_desc:
        cum += L
        if cum >= half:
            n50 = L
            break
    return n50, stat.mean(lengths), stat.median(lengths), len(lengths)


def plot_histogram(lengths, sample_name, outdir):
    """Plot and save a histogram of read lengths for one sample."""
    plt.figure()
    plt.hist(lengths, bins=50)
    plt.title(f'Read Length Distribution: {sample_name}')
    plt.xlabel('Read length (bp)')
    plt.ylabel('Count')
    out_file = os.path.join(outdir, f'{sample_name}_histogram.png')
    plt.savefig(out_file)
    plt.close()


def plot_ecdf(lengths, sample_name, outdir):
    """Plot and save an ECDF of read lengths for one sample."""
    sorted_l = sorted(lengths)
    n = len(sorted_l)
    yvals = [i / n for i in range(1, n+1)]
    plt.figure()
    plt.step(sorted_l, yvals, where='post')
    plt.title(f'ECDF of Read Lengths: {sample_name}')
    plt.xlabel('Read length (bp)')
    plt.ylabel('Fraction of reads ≤ length')
    out_file = os.path.join(outdir, f'{sample_name}_ecdf.png')
    plt.savefig(out_file)
    plt.close()


def overlay_histograms(lengths_dict, outdir):
    """Plot and save overlayed histograms for all samples."""
    plt.figure()
    for name, lengths in lengths_dict.items():
        plt.hist(lengths, bins=50, alpha=0.5, label=name)
    plt.title('Overlayed Read Length Histograms')
    plt.xlabel('Read length (bp)')
    plt.ylabel('Count')
    plt.legend()
    out_file = os.path.join(outdir, 'overlay_histogram.png')
    plt.xlim(0,50000)
    plt.savefig(out_file)
    plt.close()


def overlay_ecdf(lengths_dict, outdir):
    """Plot and save overlayed ECDFs for all samples."""
    plt.figure()
    for name, lengths in lengths_dict.items():
        sorted_l = sorted(lengths)
        n = len(sorted_l)
        yvals = [i / n for i in range(1, n+1)]
        plt.step(sorted_l, yvals, where='post', label=name)
    plt.title('Overlayed ECDF of Read Lengths')
    plt.xlabel('Read length (bp)')
    plt.ylabel('Fraction of reads ≤ length')
    plt.legend()
    out_file = os.path.join(outdir, 'overlay_ecdf.png')
    plt.xlim(0,50000)
    plt.savefig(out_file)
    plt.close()


def main():
    parser = argparse.ArgumentParser(description='Calculate N50 and plot histograms/ECDFs for BAM files.')
    parser.add_argument('--outdir', required=True,
                        help='Parent directory under which a subdirectory "n50_outputs" will be created for all plots.')
    parser.add_argument('bam_files', nargs='+', help='Paths to BAM files.')
    args = parser.parse_args()

    # Create output subdirectory
    output_parent = args.outdir
    output_sub = os.path.join(output_parent, 'n50_outputs')
    os.makedirs(output_sub, exist_ok=True)

    lengths_map = {}

    for bam_path in args.bam_files:
        sample = os.path.basename(bam_path).rsplit('.', 1)[0]
        try:
            lengths = get_read_lengths(bam_path)
            n50, mean, median, count = compute_stats(lengths)
            print(f"{sample}\tN50={n50}bp, mean={mean:.1f}bp, median={median}bp, reads={count}")

            # Individual plots
            plot_histogram(lengths, sample, output_sub)
            plot_ecdf(lengths, sample, output_sub)

            lengths_map[sample] = lengths
        except Exception as e:
            print(f"Error with {bam_path}: {e}", file=sys.stderr)

    # Overlay plots
    if lengths_map:
        overlay_histograms(lengths_map, output_sub)
        overlay_ecdf(lengths_map, output_sub)

if __name__ == '__main__':
    main()
