from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator


# TODO: clase PrestamoEntrada (BaseModel) con las 6 variables del modelo, con sus rangos (ver enunciado).
#       Debe rechazar campos que no existan.
class PrestamoEntrada(BaseModel):
    model_cofig = ConfigDict(extra="forbid")

    edad: int = Field(ge=18, le= 75)
    ingresos_mensuales: float = Field(gt= 0)
    importe_prestamo: float = Field(gt = 0)
    plazo_meses: int = Field(ge=6, le=84)
    antiguedad_laboral_anios: int= Field(ge=0, le=50)
    impagos_avios: int = Field(ge= 0, le= 20)


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
    if(value is not None > edad - 16):
        raise ValueError("Siendo menor ha trabajado")
    return value

# TODO: clase PrediccionSalida con probabilidad_impago (entre 0 y 1) y decision (aprobar, revisar o rechazar).
class PrestamoSalida(BaseModel):
    model_cofig = ConfigDict(extra="forbid")

    probabilidad_impago: float=Field(ge=0, le=1)
    decision = Literal["aprobar", "revisar", "recharzar"]
    
    
