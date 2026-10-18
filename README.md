# Emergency Route Optimizer

A Data Structures and Algorithms project comparing advanced priority queues
for shortest-path computation on a weighted road network.

## Objective

Implement and compare four priority queue data structures using a shared
Dijkstra shortest-path algorithm and a common graph dataset.

## Priority Queue Implementations

- Binomial Heap — Aswath
- Leftist Heap — Abhijith
- Radix Heap — Pranav
- Skew Heap — Hrishabh

## Planned Components

- Weighted road graph representation
- Shared Dijkstra shortest-path algorithm
- Four independently implemented priority queues
- Correctness tests and benchmark framework
- Performance analysis and visualizations

## Project Structure

- `src/ero/graph/` — graph representation and loading
- `src/ero/queues/` — priority queue interface and implementations
- `src/ero/algorithms/` — shortest-path algorithms
- `src/ero/benchmarks/` — benchmark execution and analysis
- `src/ero/visualization/` — plots and visual outputs
- `tests/` — automated correctness tests
- `data/` — datasets and small sample graphs
- `docs/` — design decisions and project documentation
- `results/` — final benchmark outputs and figures

## Setup

Requires Python 3.10 or later.

Create and activate a virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate

Install dependencies:

    python -m pip install -r requirements.txt

## Initial Scope

The initial implementation uses non-negative integer edge weights representing
road distance in metres. All priority queues will use the same graph inputs
and shortest-path workload.

## Project Status

Initial repository scaffold. Implementations and benchmark results are pending.
