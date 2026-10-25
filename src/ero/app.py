
"""Flask API and web application for Emergency Route Optimizer."""

import os
import time
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from ero.algorithms.shortest_path import (
    dijkstra_with_predecessors,
    reconstruct_path,
)
from ero.graph.location_search import (
    build_location_index,
    resolve_selection,
    search_locations,
)
from ero.graph.osm_loader import load_road_graph
from ero.queues.binomial_heap import BinomialHeap
from ero.queues.leftist_heap import LeftistHeap
from ero.queues.radix_heap import RadixHeap
from ero.queues.skew_heap import SkewHeap

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = Path(
    os.environ.get(
        "ERO_OSM_FILE",
        str(BASE_DIR / "data" / "coimbatore_roads.osm"),
    )
)

app = Flask(__name__)

HEAP_FACTORIES = {
    "radix": RadixHeap,
    "binomial": BinomialHeap,
    "leftist": LeftistHeap,
    "skew": SkewHeap,
}

# Load the graph and searchable OSM index once, when the server starts.
GRAPH = load_road_graph(DATA_FILE)
LOCATION_INDEX = build_location_index(DATA_FILE, GRAPH)


def serialize_location(result):
    """Convert an OSM search result into JSON-safe data."""
    output = {
        "name": result["name"],
        "kind": result["kind"],
    }

    if result["kind"] == "place":
        output["coordinates"] = list(result["coordinates"])

    return output


def calculate_route(start_result, destination_result, heap_name):
    """Calculate a route and return its distance, geometry and timing."""
    if heap_name not in HEAP_FACTORIES:
        raise ValueError("Unknown heap. Choose radix, binomial, leftist or skew.")

    start_node, start_snap = resolve_selection(GRAPH, start_result)
    destination_node, destination_snap = resolve_selection(
        GRAPH, destination_result
    )

    started = time.perf_counter()
    distances, predecessors = dijkstra_with_predecessors(
        GRAPH, start_node, HEAP_FACTORIES[heap_name]()
    )
    elapsed_ms = (time.perf_counter() - started) * 1000

    distance = distances[destination_node]

    if distance == float("inf"):
        raise ValueError("No route connects these locations in the loaded map.")

    path = reconstruct_path(predecessors, start_node, destination_node)

    coordinates = [
        list(GRAPH.coordinates[node_id])
        for node_id in path
        if node_id in GRAPH.coordinates
    ]

    return {
        "heap": heap_name,
        "distance_m": int(distance),
        "elapsed_ms": round(elapsed_ms, 3),
        "path": path,
        "coordinates": coordinates,
        "start_node": start_node,
        "destination_node": destination_node,
        "start_snap_m": start_snap,
        "destination_snap_m": destination_snap,
        "graph_nodes": len(GRAPH),
    }


@app.get("/")
def home():
    return render_template("index.html")


@app.get("/api/health")
def health():
    return jsonify({
        "status": "ok",
        "graph_nodes": len(GRAPH),
        "named_places": len(LOCATION_INDEX["places"]),
        "named_roads": len(LOCATION_INDEX["roads"]),
    })


@app.get("/api/search")
def search():
    query = request.args.get("q", "").strip()

    if len(query) > 100:
        return jsonify({"error": "Search query is too long."}), 400

    matches = search_locations(LOCATION_INDEX, query, limit=10)
    return jsonify([serialize_location(item) for item in matches])


@app.post("/api/route")
def route():
    payload = request.get_json(silent=True) or {}
    start_name = payload.get("start", "").strip()
    destination_name = payload.get("destination", "").strip()
    heap_name = payload.get("heap", "radix").strip().lower()

    if not start_name or not destination_name:
        return jsonify({"error": "Select both a start and destination."}), 400

    if len(start_name) > 200 or len(destination_name) > 200:
        return jsonify({"error": "Location name is too long."}), 400

    try:
        start_matches = search_locations(LOCATION_INDEX, start_name, limit=50)
        destination_matches = search_locations(
            LOCATION_INDEX, destination_name, limit=50
        )

        start_result = next(
            (item for item in start_matches
             if item["name"].casefold() == start_name.casefold()),
            None,
        )
        destination_result = next(
            (item for item in destination_matches
             if item["name"].casefold() == destination_name.casefold()),
            None,
        )

        if start_result is None or destination_result is None:
            return jsonify({
                "error": "Location not found. Choose a result from search."
            }), 404

        result = calculate_route(start_result, destination_result, heap_name)
        return jsonify(result)

    except (ValueError, KeyError) as error:
        return jsonify({"error": str(error)}), 400


@app.post("/api/compare")
def compare():
    payload = request.get_json(silent=True) or {}
    start_name = payload.get("start", "").strip()
    destination_name = payload.get("destination", "").strip()

    if not start_name or not destination_name:
        return jsonify({"error": "Select both a start and destination."}), 400

    try:
        start_matches = search_locations(LOCATION_INDEX, start_name, limit=50)
        destination_matches = search_locations(
            LOCATION_INDEX, destination_name, limit=50
        )

        start_result = next(
            (item for item in start_matches
             if item["name"].casefold() == start_name.casefold()),
            None,
        )
        destination_result = next(
            (item for item in destination_matches
             if item["name"].casefold() == destination_name.casefold()),
            None,
        )

        if start_result is None or destination_result is None:
            return jsonify({
                "error": "Location not found. Choose a result from search."
            }), 404

        results = []
        for heap_name in HEAP_FACTORIES:
            results.append(
                calculate_route(start_result, destination_result, heap_name)
            )

        distances = {result["distance_m"] for result in results}
        if len(distances) != 1:
            return jsonify({
                "error": "Heap implementations returned inconsistent distances.",
                "results": results,
            }), 500

        results.sort(key=lambda result: result["elapsed_ms"])

        return jsonify({
            "results": results,
            "correctness": "All four heaps returned the same shortest distance.",
        })

    except (ValueError, KeyError) as error:
        return jsonify({"error": str(error)}), 400


if __name__ == "__main__":
    app.run(debug=True, port=5000)
