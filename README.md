# Emergency Route Optimizer

A Data Structures and Algorithms project comparing four advanced priority queues
for shortest-path computation on a weighted road network of Coimbatore.

## Objective

The project compares Binomial, Leftist, Radix, and Skew Heaps using the same
Dijkstra shortest-path algorithm and road graph. This isolates the priority
queue implementation as the main variable in the performance comparison.

## Priority Queue Implementations

| Priority Queue | Team Member |
|---|---|
| Binomial Heap | Aswath |
| Leftist Heap | Abhijith |
| Radix Heap | Pranav |
| Skew Heap | Hrishabh |

All four heaps implement a common interface supporting insertion, minimum
extraction, and empty-heap checks.

## Features

- Road graph loaded from OpenStreetMap XML data.
- Shared Dijkstra shortest-path algorithm.
- Shortest-distance and predecessor-based route reconstruction.
- Four independently implemented priority queues.
- Automated correctness and integration tests.
- Benchmarking with repeated trials and operation counts.
- CSV benchmark output and performance comparison chart.
- Interactive menu for route calculation and heap comparison.

## Project Structure

- `src/ero/graph/` — road graph and OpenStreetMap loader
- `src/ero/queues/` — heap interface and four heap implementations
- `src/ero/algorithms/` — Dijkstra and shortest-path reconstruction
- `src/ero/demo.py` — interactive application
- `tests/` — unit and integration tests
- `benchmarks/` — benchmark runner and plotting script
- `data/` — Coimbatore road network dataset
- `results/` — benchmark CSV and comparison chart

## Setup

The project was tested with Python 3.10 or later. Install the dependencies
listed in `requirements.txt` in your Python environment:

    python3 -m pip install -r requirements.txt

Run commands from the repository root. If using a virtual environment,
activate it before running the commands below.

## Run the Application

    PYTHONPATH=src python3 -m ero.demo

The interactive menu offers:

1. Radix Heap
2. Binomial Heap
3. Leftist Heap
4. Skew Heap
5. Compare all four heaps
0. Exit

For route calculation, enter the start and destination road-node IDs. The
application reports the shortest road distance and reconstructed node path.
Default node IDs are provided for a sample route.

## Run Tests

    PYTHONPATH=src python3 -m unittest discover -s tests -v

The test suite covers heap operations, edge cases, Dijkstra integration,
shortest-path reconstruction, and consistency across all four heaps.

## Run Benchmarks

    PYTHONPATH=src python3 benchmarks/benchmark_heaps.py

The benchmark runs Dijkstra with each heap over the same road graph, repeats
the workload five times, checks that shortest-distance results match, and
records median and mean runtime along with push and pop counts.

The results are written to `results/benchmark_results.csv`.

Generate the comparison chart with:

    PYTHONPATH=src python3 benchmarks/plot_results.py

The chart is saved to `results/benchmark_comparison.png`.

## Initial Benchmark Results

The recorded experiment used a Coimbatore road graph with 2,131 locations and
3,982 directed edges. Each heap was tested five times on the same Dijkstra
workload.

| Heap | Median Runtime (ms) | Pushes | Pops |
|---|---:|---:|---:|
| Skew Heap | 7.557 | 1,881 | 1,881 |
| Radix Heap | 8.803 | 1,881 | 1,881 |
| Leftist Heap | 13.271 | 1,881 | 1,881 |
| Binomial Heap | 13.748 | 1,881 | 1,881 |

These are results from one initial experiment, not a universal ranking of heap
performance. Runtime can vary with the source location, graph, machine, Python
environment, and number of repetitions. Rerunning the benchmark may produce
different measurements.

All four implementations returned identical shortest distances in the
benchmark's correctness check.

## Scope and Limitations

Road-edge weights represent non-negative integer road distances in metres.
The computed shortest route therefore minimizes distance, not emergency
response time, traffic delay, or other real-world travel costs.

The benchmark measures the Dijkstra workload after the graph has been loaded;
graph-loading time is not included in the reported heap runtimes.
