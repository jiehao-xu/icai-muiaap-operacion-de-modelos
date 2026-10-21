"""CLI local para consumir un bundle serializado sobre un CSV."""

from __future__ import annotations

import argparse
import csv
import os
import sys
import tempfile
from pathlib import Path

from pydantic import ValidationError

from model_packaging.artifact import (
    DEFAULT_BUNDLE_PATH,
    infer_wine_quality,
    load_model_bundle,
)
from model_packaging.contracts import WineQualityRequest
from model_packaging.preprocess import FEATURE_NAMES

OUTPUT_FIELDS = (
    "sample_id",
    "quality_band",
    "confidence",
    "model_version",
    "preprocessing_version",
)
INPUT_FIELDS = ("sample_id", *FEATURE_NAMES)


def _validate_fieldnames(fieldnames: list[str] | None) -> None:
    """Rechaza columnas faltantes, desconocidas o duplicadas antes de iterar."""

    if not fieldnames:
        raise ValueError("El CSV de entrada debe incluir una cabecera.")
    if len(fieldnames) != len(set(fieldnames)):
        raise ValueError("El CSV de entrada contiene columnas duplicadas.")

    missing = [field for field in INPUT_FIELDS if field not in fieldnames]
    unknown = [field for field in fieldnames if field not in INPUT_FIELDS]
    if missing:
        raise ValueError(f"Faltan columnas obligatorias: {', '.join(missing)}.")
    if unknown:
        raise ValueError(f"Columnas no permitidas: {', '.join(unknown)}.")


def _write_csv_atomically(
    output_path: Path, rows: list[dict[str, str | float]]
) -> None:
    """Escribe el resultado en un temporal y lo publica solo al terminar."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    file_descriptor, temporary_name = tempfile.mkstemp(
        dir=output_path.parent,
        prefix=f".{output_path.name}.",
        suffix=".tmp",
        text=True,
    )
    os.close(file_descriptor)
    temporary_path = Path(temporary_name)
    try:
        with temporary_path.open("w", newline="", encoding="utf-8") as target:
            writer = csv.DictWriter(target, fieldnames=OUTPUT_FIELDS)
            writer.writeheader()
            writer.writerows(rows)
        os.replace(temporary_path, output_path)
    finally:
        temporary_path.unlink(missing_ok=True)


def predict_file(
    input_path: Path,
    output_path: Path,
    bundle_path: Path,
) -> int:
    """Valida todas las filas y escribe un CSV de predicciones completo."""

    bundle = load_model_bundle(bundle_path)
    predictions: list[dict[str, str | float]] = []

    with input_path.open(newline="", encoding="utf-8") as source:
        rows = csv.DictReader(source)
        _validate_fieldnames(rows.fieldnames)
        for row_number, row in enumerate(rows, start=2):
            sample_id = (row.get("sample_id") or "").strip()
            if not sample_id:
                raise ValueError(f"Fila {row_number} tiene un sample_id vacío.")

            model_row = {key: value for key, value in row.items() if key != "sample_id"}
            try:
                request = WineQualityRequest.model_validate(model_row)
            except ValidationError as error:
                raise ValueError(
                    f"Fila {row_number} inválida para sample_id={sample_id}: {error}"
                ) from error

            prediction = infer_wine_quality(bundle, request)
            predictions.append({"sample_id": sample_id, **prediction.model_dump()})

    _write_csv_atomically(output_path, predictions)
    return len(predictions)


def parse_args() -> argparse.Namespace:
    """Declara la interfaz pública del comando."""

    parser = argparse.ArgumentParser(
        description="Inferencia local con un bundle serializado."
    )
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--bundle", default=DEFAULT_BUNDLE_PATH, type=Path)
    return parser.parse_args()


def main() -> int:
    """Ejecuta el comando y transforma fallos de contrato en salida CLI."""

    arguments = parse_args()
    try:
        count = predict_file(
            input_path=arguments.input,
            output_path=arguments.output,
            bundle_path=arguments.bundle,
        )
    except (FileNotFoundError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 2

    print(f"Predicciones escritas: {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
