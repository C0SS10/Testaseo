import argparse

def parse_args():
    """
    Parsea los argumentos de línea de comandos.

    Returns:
        argparse.Namespace: Objeto con los argumentos procesados.
    """
    parser = argparse.ArgumentParser(description="Ejecutor de pruebas con Testa")

    parser.add_argument(
        "--types",
        "-t",
        type=str,
        default=None,
        help=(
            "Categorías de pruebas a ejecutar, separadas por coma. "
            "Ejemplo: unit,integration,e2e"
        ),
    )

    parser.add_argument(
        "--workers",
        "-w",
        type=int,
        default=4,
        help="Número máximo de workers por categoría. (default: 4)",
    )

    parser.add_argument(
        "--dir",
        "-d",
        type=str,
        default="tests",
        help="Directorio donde se encuentran las pruebas. (default: tests)",
    )

    return parser.parse_args()