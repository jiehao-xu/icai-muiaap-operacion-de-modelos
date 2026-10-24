from fastapi import APIRouter

from app.schemas.prestamo import PrediccionSalida, PrestamoEntrada
from app.services.modelo import predecir

router = APIRouter()


# TODO: POST /predict (entrada PrestamoEntrada, salida PrediccionSalida)
@router.post("predict")
def predict(payload):
    try:
        entrada = PrestamoEntrada(payload)
        preprocesado = preprocesado()
        prediccion = PrediccionSalida(model_predict(preprocesado))