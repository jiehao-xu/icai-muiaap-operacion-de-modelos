import json

from pydantic import ValidationError

from app.schemas.chat import ChatSalida, HerramientaUsada
from app.schemas.prestamo import PrestamoEntrada
from app.services.modelo import predecir

NOMBRE_TOOL = "calcular_riesgo_impago"
MAX_VUELTAS = 4

SISTEMA = (
    "Eres un asistente de riesgo de un banco. Cuando tengas todos los datos de una solicitud de "
    "prestamo, llama a la herramienta calcular_riesgo_impago. Si falta algun dato, pidelo. "
    "Nunca inventes valores. Responde en espanol y de forma breve."
)


def leer_argumentos(texto):
    """YA HECHO: convierte el texto JSON de la tool en dict ({} si no es JSON valido)."""
    try:
        datos = json.loads(texto)
    except (json.JSONDecodeError, TypeError):
        return {}
    if isinstance(datos, dict):
        return datos
    return {}


# TODO: definir_tool() -> dict con la definicion de la tool, sacando "parameters" de PrestamoEntrada
def definir_tool() -> dict:
    return {
        "type": "function",
        "function": {
            "name": NOMBRE_TOOL,
            "description": "Predice la probabilidad de impago de un préstamo",
            "parameters": PrestamoEntrada.model_json_schema()
        }
    }
# TODO: ejecutar_tool(nombre, argumentos_json) -> dict con "ok" True/False
#       (tool desconocida, JSON roto, datos invalidos o campos inventados -> ok False con el error)
def ejecutar_tool(nombre, argumentos_json) -> dict:

    if nombre != NOMBRE_TOOL:
        return {"ok": False, "error": "tool desconocida"}

    datos = leer_argumentos(argumentos_json)

    try:
        datos_validados = PrestamoEntrada(**datos)
    except ValidationError as error:
        return {"ok": False, "error": str(error)}

    try:
        result = predecir(datos_validados)
        return {
            "ok": True,
            "probabilidad_impago": result.probabilidad_impago,
            "decision": result.decision,
        }
    except Exception:
        # La frontera de la tool convierte los fallos del modelo en un resultado para el LLM.
        return {"ok": False, "error": "No se ha podido calcular el riesgo: fallo del modelo."}
# TODO: responder(mensajes, llm) -> ChatSalida, con el bucle LLM -> tool -> LLM (maximo MAX_VUELTAS)
def responder(mensajes, llm) -> ChatSalida:
    historial = [{"role": "system", "content": SISTEMA}]
    historial.extend(mensaje.model_dump() for mensaje in mensajes)

    herramientas = [definir_tool()]
    ultima_herramienta = None

    for _ in range(MAX_VUELTAS):
        respuesta_llm = llm.completar(historial, herramientas)
        llamadas = respuesta_llm.get("tool_calls") or []

        # Si el LLM responde con texto, terminamos.
        if not llamadas:
            return ChatSalida(
                respuesta=respuesta_llm.get("content") or "No se ha recibido una respuesta.",
                herramienta=ultima_herramienta,
            )

        # Guardamos la petición del asistente antes de sus resultados.
        historial.append(respuesta_llm)

        for llamada in llamadas:
            nombre = llamada["function"]["name"]
            argumentos_json = llamada["function"]["arguments"]

            resultado = ejecutar_tool(nombre, argumentos_json)

            ultima_herramienta = HerramientaUsada(
                nombre=nombre,
                argumentos=leer_argumentos(argumentos_json),
                resultado=resultado,
            )

            historial.append({
                "role": "tool",
                "tool_call_id": llamada["id"],
                "content": json.dumps(resultado, ensure_ascii=False),
            })

    return ChatSalida(
        respuesta="No se ha podido completar la operación en el máximo de intentos.",
        herramienta=ultima_herramienta,
    )
