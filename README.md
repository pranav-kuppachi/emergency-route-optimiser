# Emergency Route Optimizer

An interactive Data Structures and Algorithms project that compares four priority queue implementations for shortest-path computation on Coimbatore's OpenStreetMap road network.

Emergency Route Optimizer (ERO) uses a shared implementation of Dijkstra's algorithm with four interchangeable heaps: **Binomial Heap, Leftist Heap, Skew Heap, and Radix Heap**. It provides route calculation, shortest-path reconstruction, and performance comparison through a Flask web interface and a terminal-based demo.

## Project Objectives

- Implement and compare four priority queue data structures.
- Evaluate their performance using the same graph and shortest-path algorithm.
- Verify that all four implementations produce consistent shortest-distance results.
- Visualize routes and compare measured execution times.
- Explore the practical trade-offs between priority queue implementations.

## Priority Queue Implementations

| Priority Queue | Team Member |
|---|---|
| Binomial Heap | Aswath |
| Leftist Heap | Abhijith |
| Radix Heap | Pranav |
| Skew Heap | Hrishabh |

Each heap follows a common priority queue interface, allowing the shortest-path algorithm to use different implementations without changing its core logic.

## Features

- Loads a road network from OpenStreetMap XML data.
- Calculates shortest-distance routes using Dijkstra's algorithm.
- Reconstructs paths using predecessor information.
- Provides an interactive Flask web interface with a map.
- Supports location search and route selection.
- Compares all four heaps using the same routing workload.
- Displays measured execution times for route calculations.
- Includes a terminal-based demonstration menu.
- Provides automated tests for heap operations, edge cases, and shortest-path correctness.
- Generates benchmark results in CSV format and a comparison chart.

## Technology Stack

- **Language:** Python
- **Web framework:** Flask
- **Mapping:** Leaflet
- **Road network:** OpenStreetMap XML
- **Testing:** pytest
- **Benchmark visualization:** Matplotlib

## Project Structure

```text
emergency-route-optimiser/
├── benchmarks/
│   ├── benchmark_heaps.py
│   └── plot_results.py
├── data/
│   └── coimbatore_roads.osm
├── results/
│   ├── benchmark_comparison.png
│   └── benchmark_results.csv
├── src/
│   └── ero/
│       ├── algorithms/
│       ├── graph/
│       ├── queues/
│       ├── static/
│       ├── templates/
│       ├── app.py
│       └── demo.py
├── tests/
│   ├── algorithms/
│   ├── graph/
│   └── queues/
├── pyproject.toml
├── requirements.txt
└── README.md
```

### Main Components

- `src/ero/algorithms/` — Dijkstra's algorithm and shortest-path reconstruction.
- `src/ero/graph/` — road graph representation, OpenStreetMap loading, and location search.
- `src/ero/queues/` — common priority queue interface and heap implementations.
- `src/ero/app.py` — Flask application and routing API.
- `src/ero/demo.py` — terminal-based demonstration.
- `src/ero/templates/` — web interface HTML.
- `src/ero/static/` — frontend styling.
- `tests/` — automated unit and integration tests.
- `benchmarks/` — benchmark execution and plotting scripts.
- `data/` — road network dataset.
- `results/` — recorded benchmark outputs.

## Requirements

- Python 3.9 or later.
- pip.
- Internet access for loading the web map's external Leaflet assets, unless those assets are otherwise available locally.

Run commands from the repository root.

## Installation

Clone the repository:

```bash
git clone https://github.com/pranav-kuppachi/emergency-route-optimiser.git
cd emergency-route-optimiser
```

Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run the Web Application

Start the Flask application:

```bash
PYTHONPATH=src python -m ero.app
```

Open the local address printed by Flask in your browser. The interface allows you to search for locations, calculate routes, and compare the four priority queue implementations.

The road network is loaded when the application starts. By default, the application uses `data/coimbatore_roads.osm`.

To use a different compatible OSM XML dataset, set `ERO_OSM_FILE` to its path before starting the application:

```bash
ERO_OSM_FILE=/path/to/road-network.osm PYTHONPATH=src python -m ero.app
```

## Run the Terminal Demo

```bash
PYTHONPATH=src python -m ero.demo
```

The interactive menu provides:

1. Radix Heap
2. Binomial Heap
3. Leftist Heap
4. Skew Heap
5. Compare all four heaps
0. Exit

For route calculations, the terminal demo uses road-node IDs. Follow the prompts and use the sample IDs provided by the application where applicable.

## Run Tests

Run the automated test suite with pytest:

```bash
PYTHONPATH=src python -m pytest -q
```

The current project test suite has passed **63 tests** in the development environment.

The tests cover priority queue operations, edge cases, Dijkstra integration, shortest-path reconstruction, graph loading, location search, and consistency across heap implementations.

## Run Benchmarks

Execute the benchmark runner:

```bash
PYTHONPATH=src python benchmarks/benchmark_heaps.py
```

Generate the comparison chart:

```bash
PYTHONPATH=src python benchmarks/plot_results.py
```

The benchmark workflow runs the shortest-path workload with each heap over the same road graph, performs repeated trials, checks the resulting shortest distances, and records runtime and operation counts.

Outputs are saved to:

- `results/benchmark_results.csv`
- `results/benchmark_comparison.png`

## Recorded Benchmark Results

The initial recorded experiment used a Coimbatore road graph containing 2,131 locations and 3,982 directed edges. Each heap was tested five times on the same workload.

| Heap | Median Runtime (ms) | Pushes | Pops |
|---|---:|---:|---:|
| Skew Heap | 7.557 | 1,881 | 1,881 |
| Radix Heap | 8.803 | 1,881 | 1,881 |
| Leftist Heap | 13.271 | 1,881 | 1,881 |
| Binomial Heap | 13.748 | 1,881 | 1,881 |

These values represent one recorded experiment and should be interpreted alongside the checked-in CSV and chart. They are not a universal ranking of heap performance. Results can vary with the graph, source node, hardware, Python environment, and trial conditions.

The benchmark's correctness check confirmed that all four implementations returned identical shortest-distance results for the tested workload.

## Algorithm and Evaluation Notes

All four priority queues are evaluated using the same Dijkstra shortest-path algorithm. This helps isolate the effect of the priority queue implementation while keeping the graph and routing workload consistent.

The benchmark reports measured execution time for the tested workload. Theoretical time and space complexity are separate analytical measures and should not be confused with empirical runtime or memory measurements.

## Scope and Limitations

- Edge weights represent non-negative integer road distances in metres.
- The computed route minimizes **distance**, not estimated emergency response time.
- The application does not model live traffic, road closures, ambulance-specific restrictions, or real-time emergency conditions.
- The benchmark measures the Dijkstra workload after graph loading; initial dataset-loading time is excluded from the reported heap runtimes.
- Results are dependent on the dataset and benchmark conditions.

## Future Improvements

- Expand evaluation across multiple source-destination pairs and graph sizes.
- Add more systematic runtime and memory comparisons.
- Improve benchmark reproducibility and statistical analysis.
- Explore routing weights that account for additional real-world travel factors.

## Academic Context

This project was developed as a Data Structures and Algorithms case study to investigate how priority queue design affects Dijkstra's shortest-path computation on a real-world road network.
