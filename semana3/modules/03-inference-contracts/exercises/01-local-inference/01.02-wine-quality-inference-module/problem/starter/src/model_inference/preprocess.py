"""Transformación de una muestra validada en el vector del modelo."""

from dataclasses import dataclass

from model_inference.contracts import WineQualityRequest

PREPROCESSING_VERSION = "wine-red-features-v1"

# Este contrato se entrega ya decidido: no cambies ni los nombres ni el orden.
FEATURE_NAMES = (
    "fixed_acidity",
    "volatile_acidity",
    "citric_acid",
    "residual_sugar",
    "chlorides",
    "free_sulfur_dioxide",
    "total_sulfur_dioxide",
    "density",
    "ph",
    "sulphates",
    "alcohol",
)


@dataclass(frozen=True)
class WineFeatures:
    fixed_acidity: float
    volatile_acidity: float
    citric_acid: float
    residual_sugar: float
    chlorides: float
    free_sulfur_dioxide: float
    total_sulfur_dioxide: float
    density: float
    ph: float
    sulphates: float
    alcohol: float

    def as_vector(self) -> list[float]:
        """Respeta el orden del artefacto, independientemente del CSV."""
        return [getattr(self, name) for name in FEATURE_NAMES]


def preprocess_wine_request(request: WineQualityRequest) -> WineFeatures:
    """Convierte el contrato de entrada en el vector del modelo entrenado."""

    return WineFeatures(**request.model_dump())
