import time
from testa.parsers.argument_parser import parse_args
from testa.parsers.test_types_parser import parse_types
from testa.runner import discover_tests, run_all_tests
from dotenv import load_dotenv


def main() -> None:
    """Ejecuta el runner de Testa."""
    load_dotenv()

    args = parse_args()
    types = parse_types(args.types)

    discover_tests(args.dir)

    print(
        f"Ejecutando categorías: {types or 'todas'} "
        f"con {args.workers} worker(s) por categoría.\n"
    )

    start = time.perf_counter()

    run_all_tests(types=types, max_workers=args.workers)

    end = time.perf_counter()
    elapsed = end - start

    print(f"\n⏱ Tiempo total: {elapsed:.3f} segundos")


if __name__ == "__main__":
    main()