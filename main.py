import time
import argparse
from testa.runner import discover_tests, run_all_tests
try:
    from dotenv import load_dotenv
except Exception:
    # Optional dependency; continue if not installed (Poetry users will have it).
    def load_dotenv():
        return None


def _parse_args():
    parser = argparse.ArgumentParser(description="Run Testa tests")
    parser.add_argument("--types", "-t", help="Comma-separated test categories to run (e.g. unit,integration,e2e)", default=None)
    parser.add_argument("--workers", "-w", type=int, help="Default number of workers per category", default=4)
    parser.add_argument("--dir", "-d", help="Directory where tests are located (default: tests)", default="tests")
    return parser.parse_args()


load_dotenv()


if __name__ == "__main__":
    args = _parse_args()
    types = args.types.split(",") if args.types else None

    discover_tests(args.dir)

    print(f"Running categories: {types or 'all'} with default workers per category: {args.workers}\n")

    start = time.perf_counter()
    results = run_all_tests(types=types, max_workers=args.workers)
    end = time.perf_counter()

    elapsed = end - start
    print(f"\n⏱ Total time: {elapsed:.3f} seconds")