
import csv
from pathlib import Path

import matplotlib.pyplot as plt


ROOT = Path(__file__).resolve().parents[1]
CSV_FILE = ROOT / "results" / "benchmark_results.csv"
OUTPUT_FILE = ROOT / "results" / "benchmark_comparison.png"


def main():
    with open(CSV_FILE, newline="") as file:
        rows = list(csv.DictReader(file))

    rows.sort(key=lambda row: float(row["median_seconds"]))

    names = [row["heap"] for row in rows]
    times_ms = [
        float(row["median_seconds"]) * 1000
        for row in rows
    ]

    plt.figure(figsize=(9, 5))
    plt.bar(names, times_ms)
    plt.ylabel("Median execution time (milliseconds)")
    plt.xlabel("Priority queue")
    plt.title("Dijkstra Performance on Coimbatore Road Network")
    plt.tight_layout()

    OUTPUT_FILE.parent.mkdir(exist_ok=True)
    plt.savefig(OUTPUT_FILE, dpi=200)
    plt.close()

    print("Chart saved to:", OUTPUT_FILE)


if __name__ == "__main__":
    main()
