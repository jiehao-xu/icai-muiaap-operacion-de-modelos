"""TODO: contratos de entrada y salida de la inferencia."""

# Implementa WineQualityRequest y WineQualityPrediction con Pydantic.
# Revisa los campos de assets/inference_samples.csv y prohíbe columnas extra.

from pypantic import BaseModel, Field, field_validator
import pandas as pd

class WineQualityRequest(BaseModel):
    sample_id: int = Field(..., description="Unique identifier for the wine sample")
    fixed_acidity: float = Field(..., description="Fixed acidity of the wine sample")
    volatile_acidity: float = Field(..., example = 0.5, description="Volatile acidity of the wine sample")
    citric_acid: float = Field(..., description="Citric acid content of the wine sample")
    residual_sugar: float = Field(..., description="Residual sugar content of the wine sample")
    chlorides: float = Field(..., description="Chloride content of the wine sample")
    free_sulfur_dioxide: float = Field(..., description="Free sulfur dioxide content of the wine sample")
    total_sulfur_dioxide: float = Field(..., description="Total sulfur dioxide content of the wine sample")
    density: float = Field(..., description="Density of the wine sample")
    ph: float = Field(..., description="pH value of the wine sample")
    sulphates: float = Field(..., description="Sulphate content of the wine sample")
    alcohol: float = Field(..., description="Alcohol content of the wine sample")

class WineQualityPrediction(BaseModel):
    quality: float = Field(..., description="Predict quality score")
