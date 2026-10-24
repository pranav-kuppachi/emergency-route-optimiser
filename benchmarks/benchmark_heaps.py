#This file compares Execution time, Pushes and pops, Correctness, Repeated trials and
# CSV output among all 4 heaps.


import csv
import statistics
import time
from pathlib import Path

from ero.graph.osm_loader import load_road_graph
from ero.algorithms.dijkstra import dijkstra
from ero.queues.binomial_heap import BinomialHeap
from ero.queues.leftist_heap import LeftistHeap
from ero.queues.radix_heap import RadixHeap
from ero.queues.skew_heap import SkewHeap


REPO_ROOT = Path(__file__).resolve().parents[1]
OSM_FILE = REPO_ROOT / "data" / "coimbatore_roads.osm"
RESULTS_DIR = REPO_ROOT / "results"
CSV_FILE = RESULTS_DIR / "benchmark_results.csv"

REPETITIONS = 5


class CountingHeap:
    def __init__(self, heap):
        self.heap = heap
        self.pushes = 0
        self.pops = 0

    def push(self, priority, item):
        self.pushes += 1
        self.heap.push(priority, item)

    def pop_min(self):
        self.pops += 1
        return self.heap.pop_min()

    def is_empty(self):
        return self.heap.is_empty()


def count_road_edges(graph):
    total = 0

    for location in graph.locations():
        total += len(graph.neighbors(location))

    return total


def main():
    print("Loading Coimbatore road network...")

    graph = load_road_graph(str(OSM_FILE))
    locations = graph.locations()

    if not locations:
        raise ValueError("The road graph contains no locations.")

    start = locations[0]

    print("Locations:", len(locations))
    print("Directed edges:", count_road_edges(graph))
    print("Starting location:", start)
    print("Benchmark repetitions:", REPETITIONS)

    heaps = {
        "Binomial Heap": BinomialHeap,
        "Leftist Heap": LeftistHeap,
        "Radix Heap": RadixHeap,
        "Skew Heap": SkewHeap,
    }

    results = []
    expected_distances = None

    for heap_name, heap_class in heaps.items():
        print("\nBenchmarking", heap_name)

        timings = []
        operation_counts = None

        for run in range(REPETITIONS):
            heap = CountingHeap(heap_class())

            start_time = time.perf_counter()
            distances = dijkstra(graph, start, heap)
            elapsed = time.perf_counter() - start_time

            if expected_distances is None:
                expected_distances = distances
            elif distances != expected_distances:
                raise AssertionError(
                    heap_name + " produced different shortest distances."
                )

            timings.append(elapsed)

            counts = (heap.pushes, heap.pops)

            if operation_counts is None:
                operation_counts = counts
            elif counts != operation_counts:
                raise AssertionError(
                    heap_name + " produced inconsistent operation counts."
                )

            print(
                "  Run", run + 1,
                "-", round(elapsed, 6), "seconds"
            )

        results.append({
            "heap": heap_name,
            "locations": len(locations),
            "directed_edges": count_road_edges(graph),
            "start_location": start,
            "repetitions": REPETITIONS,
            "median_seconds": statistics.median(timings),
            "mean_seconds": statistics.mean(timings),
            "pushes": operation_counts[0],
            "pops": operation_counts[1],
        })

        print("  Median:", round(statistics.median(timings), 6), "seconds")
        print("  Pushes:", operation_counts[0])
        print("  Pops:", operation_counts[1])

    RESULTS_DIR.mkdir(exist_ok=True)

    with open(CSV_FILE, "w", newline="") as csv_file:
        columns = results[0].keys()
        writer = csv.DictWriter(csv_file, fieldnames=columns)
        writer.writeheader()
        writer.writerows(results)

    print("\nAll four heaps returned identical shortest distances.")
    print("Results saved to:", CSV_FILE)

    print("\nFinal comparison:")
    results.sort(key=lambda result: result["median_seconds"])

    for result in results:
        print(
            result["heap"],
            "- median:",
            round(result["median_seconds"], 6),
            "seconds"
        )


if __name__ == "__main__":
    main()
