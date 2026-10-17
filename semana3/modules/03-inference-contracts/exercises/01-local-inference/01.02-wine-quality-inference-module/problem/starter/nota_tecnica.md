# Nota técnica

## 1. Validar la entrada y la salida

He usado Pydantic para comprobar que llegan las once variables esperadas, dentro de los rangos definidos y sin columnas extra, así puedo detectar errores antes de llamar al modelo. También valido la categoría y la confianza de salida e incluyo las versiones del modelo y del preprocesado para saber cómo se generó cada una de las predicciones.

## 2. Mantener el orden de las variables

Construyo el vector siguiendo `FEATURE_NAMES`, aunque las columnas del CSV lleguen en otro orden. Al cargar el modelo compruebo que sus variables coinciden en nombre y posición. Esto evita que el modelo confunda valores, como el alcohol y la acidez, y dé un resultado incorrecto sin avisar.
