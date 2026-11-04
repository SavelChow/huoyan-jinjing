"""Minimal command contract; no synthetic predictions are produced."""
import argparse
import importlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

def model_registry():
    return json.loads((ROOT / "shared" / "catalogue.json").read_text(encoding="utf-8"))["models"]

def main(argv=None):
    registry = model_registry()
    parser = argparse.ArgumentParser(description="火眼金睛 - course batch interface")
    parser.add_argument("--list-models", action="store_true")
    parser.add_argument("--input_dir")
    parser.add_argument("--model", choices=registry)
    parser.add_argument("--output_dir")
    parser.add_argument("--counts_file")
    args = parser.parse_args(argv)
    if args.list_models:
        for name, module in registry.items():
            print(f"{name}: {module}")
        return 0
    if not all((args.input_dir, args.model, args.output_dir, args.counts_file)):
        parser.error("--input_dir, --model, --output_dir and --counts_file are required")
    module = importlib.import_module(registry[args.model])
    if not callable(getattr(module, "predict", None)):
        parser.error("Model module must expose predict(image_path)")
    parser.exit(2, "NOT_IMPLEMENTED: batch input validation, inference and CSV export are pending; no output created.\n")
