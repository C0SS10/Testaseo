import time
from testa.runner import discover_tests, run_all_tests
from dotenv import load_dotenv
load_dotenv()


if __name__ == "__main__":
    discover_tests()
    for workers in (1, 8):
        print(f"\n=== Ejecutando tests con {workers} worker(s) ===")

        start = time.perf_counter()
        results = run_all_tests(max_workers=workers)
        end = time.perf_counter()

        elapsed = end - start
        print(f"⏱ Tiempo con {workers} worker(s): {elapsed:.3f} segundos")