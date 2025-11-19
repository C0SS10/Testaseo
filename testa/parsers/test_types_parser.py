from typing import List, Optional


def parse_types(types_arg: Optional[str]) -> Optional[List[str]]:
    """
    Convierte el argumento de tipos en una lista de strings.

    Args:
        types_arg (Optional[str]): Cadena separada por comas, o None.

    Returns:
        Optional[List[str]]: Lista de categorías o None si no se especifica.
    """
    if not types_arg:
        return None

    types = [t.strip() for t in types_arg.split(",") if t.strip()]

    return types if types else None
