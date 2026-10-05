"""TODO: transformación de una muestra validada en el vector del modelo."""

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

# Implementa WineFeatures y preprocess_wine_request(). El orden anterior debe
# coincidir con el artefacto, no con un orden arbitrario del CSV.

import pandas
from contracts import WineQualityRequest

class WineFeatures:

    fixed_acidity: float = Field(ge=0, le=20)
    volatile_acidity: float = Field(ge=0, le=20)
    citric_acid: float = Field(ge=0, le=20)
    residual_sugar: float = Field(ge=0, le=20)
    chlorides: float = Field(ge=0, le=20)
    free_sulfur_dioxide: float = Field(ge=0, le=20)
    total_sulfur_dioxide: float = Field(ge=0, le=20)
    density: float = Field(ge=0, le=20)
    ph: float = Field(ge=0, le=20)
    sulphates: float = Field(ge=0, le=20)
    alcohol: float = Field(ge=0, le=20)

    def as_evector() -> list[float]:
        return [fixed_acidity,
            volatile_acidity,
            citric_acid,
            residual_sugar,
            chlorides,
            free_sulfur_dioxide,
            total_sulfur_dioxide,
            density,
            ph,
            sulphates,
            alcohol]

def preprocess_wine_request(
    request: WineQualityRequest
) -> WineFeatures:
    data = request.model_dump()

    return WineFeatures(
        **{
            feature: data[feature]
            for feature in FEATURE_NAMES
        }
    )




def preprocess_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    prepared_rows = []

    for _, row in df.iterrows():

        request = WineQualityRequest.model_validate(
            row.to_dict()
        )

        features = preprocess_wine_request(request)

        prepared_rows.append(
            features.as_vector()
        )

    return pd.DataFrame(
        prepared_rows,
        columns=FEATURE_NAMES
    )
