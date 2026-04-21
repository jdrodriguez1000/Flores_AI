# src/data/bronze_loader.py
# Trazable: SpecDD §6 | contract.md §2 | SAD §5.1 | backlog F2-T03a
#
# Modulo de ingesta de la Capa Bronze — Inmutabilidad garantizada.
# Lee el CSV crudo del dataset Iris sin aplicar ninguna transformacion
# de negocio ni limpieza. Bronze is Sacred.

from pathlib import Path

import pandas as pd

from src import config


def load_bronze(csv_path: Path = config.DATA_BRONZE) -> pd.DataFrame:
    """Lee el archivo CSV crudo del dataset Iris desde la Capa Bronze.

    No realiza ninguna transformacion sobre los datos. El dato se
    persiste tal cual proviene de la fuente, preservando el linaje
    y la inmutabilidad de la capa Bronze.

    Args:
        csv_path: Ruta al archivo CSV. Default: config.DATA_BRONZE.
                  Acepta inyeccion de dependencias para testabilidad.

    Returns:
        DataFrame con 150 filas y 6 columnas:
        ['Id', 'SepalLengthCm', 'SepalWidthCm', 'PetalLengthCm', 'PetalWidthCm', 'Species'].
        Tipos: int64 (Id), float64 (x4), object (Species).

    Raises:
        FileNotFoundError: Si csv_path no existe en el sistema de archivos.
        pd.errors.ParserError: Si el archivo no es un CSV valido.
    """
    if not csv_path.exists():
        raise FileNotFoundError(
            f"Archivo CSV de Bronze no encontrado: {csv_path}"
        )

    return pd.read_csv(csv_path)
