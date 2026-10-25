from pathlib import Path
import csv
import runpy

from ero.algorithms.shortest_path import (
    dijkstra_with_predecessors,
    reconstruct_path,
)
from ero.graph.osm_loader import load_road_graph
from ero.queues.binomial_heap import BinomialHeap
from ero.queues.leftist_heap import LeftistHeap
from ero.queues.radix_heap import RadixHeap
from ero.queues.skew_heap import SkewHeap


ROOT = Path(__file__).resolve().parents[2]
OSM_FILE = ROOT / "data" / "coimbatore_roads.osm"
CSV_FILE = ROOT / "results" / "benchmark_results.csv"

DEFAULT_START = 1228189707
DEFAULT_DESTINATION = 330044079

HEAPS = {
    "1": ("Radix Heap", RadixHeap),
    "2": ("Binomial Heap", BinomialHeap),
    "3": ("Leftist Heap", LeftistHeap),
    "4": ("Skew Heap", SkewHeap),
}


def find_route(graph, heap_class, start, destination):
    distances, predecessors = dijkstra_with_predecessors(
        graph, start, heap_class()
    )

    path = reconstruct_path(predecessors, start, destination)

    print("\n--- Route Results ---")
    print(f"Start node: {start}")
    print(f"Destination node: {destination}")

    if not path:
        print("No route found between these locations.")
        return

    print(f"Shortest distance: {distances[destination]:,} metres")
    print(f"Road-network nodes in path: {len(path)}")
    print("\nPath:")
    print(" -> ".join(map(str, path)))


def get_location(prompt, default, locations):
    while True:
        raw = input(f"{prompt} [default: {default}]: ").strip()

        try:
            location = default if not raw else int(raw)
        except ValueError:
            print("Please enter a valid integer road-node ID.")
            continue

        if location not in locations:
            print("That road-node ID does not exist in this dataset.")
            continue

        return location


def compare_heaps():
    print("\nRunning the four-heap benchmark.")
    print("This may take a few seconds...\n")

    # Reuse the existing benchmark implementation.
    runpy.run_path(
        str(ROOT / "benchmarks" / "benchmark_heaps.py"),
        run_name="__main__",
    )

    if not CSV_FILE.exists():
        print("Benchmark CSV was not generated.")
        return

    with CSV_FILE.open(newline="") as file:
        results = list(csv.DictReader(file))

    results.sort(key=lambda row: float(row["median_seconds"]))

    print("\n=== Performance Comparison ===")
    print(f"{'Heap':<18} {'Median (ms)':>12} {'Pushes':>10} {'Pops':>10}")
    print("-" * 54)

    for result in results:
        median_ms = float(result["median_seconds"]) * 1000
        print(
            f"{result['heap']:<18} "
            f"{median_ms:>12.3f} "
            f"{result['pushes']:>10} "
            f"{result['pops']:>10}"
        )

    print("\nFull results:", CSV_FILE)
    print("All heaps use the same graph and Dijkstra workload.")


def main():
    print("Loading Coimbatore road network...")
    graph = load_road_graph(str(OSM_FILE))
    locations = set(graph.locations())

    print("\n=== Emergency Route Optimizer ===")
    print(f"Road-network locations: {len(locations):,}")

    while True:
        print("\nChoose an option:")
        print("1. Radix Heap")
        print("2. Binomial Heap")
        print("3. Leftist Heap")
        print("4. Skew Heap")
        print("5. Compare all four heaps")
        print("0. Exit")

        choice = input("\nEnter your choice: ").strip()

        if choice == "0":
            print("Exiting Emergency Route Optimizer. Goodbye!")
            break

        if choice == "5":
            try:
                compare_heaps()
            except Exception as error:
                print(f"Benchmark failed: {error}")
            continue

        if choice not in HEAPS:
            print("Invalid option. Choose 0, 1, 2, 3, 4, or 5.")
            continue

        heap_name, heap_class = HEAPS[choice]
        print(f"\nSelected: {heap_name}")

        start = get_location(
            "Enter start road-node ID",
            DEFAULT_START,
            locations,
        )
        destination = get_location(
            "Enter destination road-node ID",
            DEFAULT_DESTINATION,
            locations,
        )

        try:
            find_route(graph, heap_class, start, destination)
        except Exception as error:
            print(f"Route computation failed: {error}")


if __name__ == "__main__":
    main()
