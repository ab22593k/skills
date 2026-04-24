#!/usr/bin/env python3
import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from hdrh.histogram import HdrHistogram
import statsmodels.api as sm

def plot_histogram(df, output):
    plt.figure(figsize=(10, 6))
    plt.hist(df["latency_secs"] * 1000, bins='auto', alpha=0.7, color='blue', edgecolor='black')
    plt.title("Latency Distribution (Histogram)")
    plt.xlabel("Latency (ms)")
    plt.ylabel(f"Frequency (N={len(df)})")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig(output, dpi=300)
    plt.close()
    print(f"Saved histogram to {output}")

def plot_hdr_histogram(df, output):
    # HDR Histogram (min=1ms, max=10000ms, sig_figs=3)
    histogram = HdrHistogram(1, 10000, 3)
    for l in df["latency_secs"]:
        histogram.record_value(int(l * 1000))
    
    percentiles = [25.0, 50.0, 75.0, 90.0, 99.0, 99.9, 99.99]
    data = []
    for p in percentiles:
        val = histogram.get_value_at_percentile(p)
        data.append([p / 100.0, val])
    
    hist_df = pd.DataFrame(data, columns=['Percentile', 'Value'])
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(hist_df["Percentile"], hist_df["Value"], marker='o')
    ax.grid(True, which='both', linestyle='--', alpha=0.6)
    ax.set_title("Latency by Percentile (HDR Histogram)")
    ax.set_xlabel("Percentile (%)")
    ax.set_ylabel("Latency (ms)")
    ax.set_xscale('logit')
    
    plt.xticks(percentiles_to_ticks(percentiles))
    labels = [f"{p}%" for p in percentiles]
    ax.xaxis.set_major_formatter(ticker.FixedFormatter(labels))
    ax.xaxis.set_minor_formatter(ticker.NullFormatter())
    
    plt.savefig(output, dpi=300)
    plt.close()
    print(f"Saved HDR histogram to {output}")

def percentiles_to_ticks(percentiles):
    return [p/100.0 for p in percentiles]

def plot_ecdf(df, output):
    values = df["latency_secs"] * 1000
    ecdf = sm.distributions.ECDF(values)
    x = np.linspace(min(values), max(values), 1000)
    y = ecdf(x)
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, color='green', linewidth=2)
    plt.title("Empirical Cumulative Distribution Function (eCDF)")
    plt.xlabel("Latency (ms)")
    plt.ylabel("Cumulative Probability")
    plt.yticks(np.arange(0, 1.1, 0.1))
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig(output, dpi=300)
    plt.close()
    print(f"Saved eCDF plot to {output}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Visualize latency distribution from CSV.")
    parser.add_argument("input", help="Input CSV file with 'latency_secs' column")
    parser.add_argument("--prefix", default="latency", help="Prefix for output image files")
    
    args = parser.parse_args()
    
    df = pd.read_csv(args.input)
    if "latency_secs" not in df.columns:
        print("Error: CSV must contain a 'latency_secs' column.")
        exit(1)
        
    plot_histogram(df, f"{args.prefix}_histogram.png")
    plot_hdr_histogram(df, f"{args.prefix}_hdr.png")
    plot_ecdf(df, f"{args.prefix}_ecdf.png")
