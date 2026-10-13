# Wine Quality Project

Proyecto de entrenamiento y evaluación de un modelo de Machine Learning sobre el dataset **Wine Quality**.

El objetivo del proyecto es organizar el código de entrenamiento como un paquete Python reproducible utilizando `uv`, incluyendo los datos, tests y herramientas de calidad de código necesarias para que el proyecto pueda ser instalado y revisado fácilmente.

## Estructura del Proyecto

```text
wine-quality-project/
│
├── data/
│   └── raw/
│       └── WineQT.csv
│
├── src/
│   └── wine_quality/
│       ├── __init__.py
│       └── train.py
│
├── tests/
│   └── test_train.py
│
├── pyproject.toml
├── uv.lock
└── README.md