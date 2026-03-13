#!/usr/bin/env python3
import argparse
import time
import pandas as pd
from ping3 import ping

def collect_pings(host, samples, interval=1.0):
    """
    Collects network latency samples using ICMP pings.
    Avoids coordinated omission by sending pings at fixed intervals.
    """
    print(f"Collecting {samples} samples from {host} at {interval}s intervals...")
    values = []
    for i in range(samples):
        # We use the interval as the timeout to ensure we stay on schedule
        value = ping(host, timeout=interval)
        if value is None:
            print(f"Sample {i}: Timeout (> {interval}s)")
            continue
        
        values.append(value)
        
        # Schedule next ping at exactly 'interval' from current start
        # value is in seconds
        sleep_time = max(0, interval - value)
        time.sleep(sleep_time)
    
    return values

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Collect latency samples avoiding coordinated omission.")
    parser.add_argument("host", help="Host to ping")
    parser.add_argument("--samples", type=int, default=100, help="Number of samples")
    parser.add_argument("--interval", type=float, default=1.0, help="Interval in seconds")
    parser.add_argument("--output", default="latency_data.csv", help="Output CSV file")
    
    args = parser.parse_args()
    
    latencies = collect_pings(args.host, args.samples, args.interval)
    
    df = pd.DataFrame({"latency_secs": latencies})
    df.to_csv(args.output, index=False)
    print(f"Saved {len(latencies)} samples to {args.output}")
