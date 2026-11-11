from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


# TODO: clase PrestamoEntrada (BaseModel) con las 6 variables del modelo, con sus rangos (ver enunciado).
#       Debe rechazar campos que no existan.
class PrestamoEntrada(BaseModel):
    model_cofig = ConfigDict(extra="forbid")

    edad: int = Field(ge=18, le= 75, description = "Edad del usuario")
    ingresos_mensuales: float = Field(gt= 0, description = "Ingresos mensuales del usuario")
    importe_prestamo: float = Field(gt = 0, description = "Importe del prestamo del usuario")
    plazo_meses: int = Field(ge=6, le=84, description = "Número de meses que tiene el usuario para devolver el prestamo")
    antiguedad_laboral_anios: int= Field(ge=0, le=50, description = "Antiguedad laboral del usuario en años")
    impagos_avios: int = Field(ge= 0, le= 20, description = "Número de veces que el usuario ha incumplido los pagos")


# TODO: field_validator (con classmethod) para antiguedad_laboral_anios: no puede ser incoherente con la edad.
# @field_validator("antiguedad_laboral_anios", mode="before")
# @classmethod()
# def antiguedad_laboral_anios(cls, value):
#     if(value > cls.edad - 16):
#         raise ValueError("Siendo menor ha trabajado")
#     return value
@field_validator("antiguedad_laboral_anios", mode="before")
@classmethod()
def antiguedad_laboral_anios(cls, value, info):
    edad = info.data.get("edad")
    if edad is not None and value is not None and value > edad - 16:
        raise ValueError("Siendo menor ha trabajado")
    return value

# TODO: clase PrediccionSalida con probabilidad_impago (entre 0 y 1) y decision (aprobar, revisar o rechazar).
class PrestamoSalida(BaseModel):
    model_cofig = ConfigDict(extra="forbid")

    probabilidad_impago: float=Field(ge=0, le=1)
    decision = Literal["aprobar", "revisar", "recharzar"]
    
    
