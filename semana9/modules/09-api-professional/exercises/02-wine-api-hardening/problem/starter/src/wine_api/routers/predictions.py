from dataclasses import asdict

from fastapi import APIRouter, Body

from typing import Annotated
from wine_api.dependencies import PredictorDep, RequestIdDep
from wine_api.schemas import PredictionRequest
from datetime import UTC, datetime
from wine_api.schemas import (
    VALID_FEATURES_EXAMPLE,
    ErrorResponse,
    Prediction,
    PredictionRequest,
    PredictionResponse,
)

# TODO S9.3a: mueve aquí `prefix="/v1/predictions"` y `tags=["predictions"]`.
# TODO S9.3c: declara a nivel de router `responses=` para 400, 422 y 503 con
# `{"model": ErrorResponse, "description": ...}`. Así el 422 deja de
# documentarse como `HTTPValidationError`, que ya no es lo que devolvemos.
router = APIRouter(
    prefix="/v1/predictions",
    tags=["predictions"],
    responses={
        400: {
            "model": ErrorResponse,
            "description": "El cuerpo de la petición no es JSON válido.",
        },
        422: {
            "model": ErrorResponse,
            "description": "Los datos de entrada incumplen el contrato.",
        },
        503: {
            "model": ErrorResponse,
            "description": "El modelo no está disponible para predecir.",
        },
    },
)


@router.post(
        "",
        summary="Predecir la calidad de un vino",
        response_description=(
            "Predicción con banda de calidad, confianza, versiones "
            "del modelo y del preprocesado, request_id y fecha UTC."
        ),

)
def create_prediction(
    payload: Annotated[
        PredictionRequest,
        Body(
            openapi_examples={
                "valid": {
                    "summary": "Petición válida",
                    "value": {"features": VALID_FEATURES_EXAMPLE},
                },
                "alcohol_out_of_range": {
                    "summary": "Inválida: alcohol fuera de rango (422)",
                    "value": {
                        "features": {
                            **VALID_FEATURES_EXAMPLE,
                            "alcohol": 25.0,
                        },
                    },
                },
                "unexpected_field": {
                    "summary": "Inválida: campo no permitido (422)",
                    "value": {
                        "features": {
                            **VALID_FEATURES_EXAMPLE,
                            "color": "red",
                        },
                    },
                },
            },
        ), # type: ignore
    ],
    predictor: PredictorDep,
    request_id: RequestIdDep,
) -> PredictionResponse:
    """Solicita una predicción a partir de once propiedades del vino.

    Envía un objeto `features` con todos los campos de WineFeatures.
    Los valores deben ser numéricos y respetar los rangos inclusivos
    documentados en el esquema; por ejemplo, alcohol entre 5 y 20 % vol.
    No se admiten campos adicionales.

    La respuesta incluye la banda de calidad y una confidence entre 0 y 1,
    redondeada a dos decimales, además de las versiones del modelo y del
    preprocesado, el request_id y served_at en UTC.

    Respuestas:
    - **200**: predicción realiszada correctamente.
    - **400**: cuerpo JSON mal formado.
    - **422**: campos ausentes, tipos incorrectos o valores no admitidos.
    - **503**: modelo no disponible.

    Los errores utilizan el sobre común ErrorResponse.
    """
    # TODO S9.3e: añade summary, response_description y un docstring útil para
    # quien consume la API (campos, rangos, decimales de confidence).
    # TODO S9.3f: ofrece en Swagger al menos tres ejemplos de cuerpo (uno válido
    # y dos inválidos). Investiga `Annotated[PredictionRequest, Body(...)]` con
    # `openapi_examples=`; usa VALID_FEATURES_EXAMPLE como base.
    
    # TODO S9.1e: este dict expone `raw_score` y la confianza sin redondear.
    # Declara `-> PredictionResponse` y construye el modelo; para pasar de la
    # dataclass ModelOutput a Prediction investiga `from_attributes=True`.
    output = predictor.predict(payload.features)
    return PredictionResponse(
        prediction=Prediction.model_validate(output, from_attributes=True),
        request_id=request_id,
        served_at=datetime.now(UTC),
    )
