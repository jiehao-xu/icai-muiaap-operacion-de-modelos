"""Starter de la primera interfaz Streamlit para Wine Quality."""

from __future__ import annotations

import os
from collections.abc import Callable
from pathlib import Path
from typing import Any

from model_ui.contracts import PredictionPayload
from model_ui.errors import ArtifactUnavailableError, InputContractError
from model_ui.gateway import InferenceGateway, PackagedBundleGateway


def build_gateway() -> InferenceGateway:
    """Carga obligatoriamente el bundle de S4 configurado."""

    bundle_value = os.getenv("MODEL_UI_BUNDLE")
    if not bundle_value:
        raise ArtifactUnavailableError("MODEL_UI_BUNDLE no está configurado.")
    try:
        return PackagedBundleGateway.from_bundle_path(Path(bundle_value))
    except Exception as error:  # noqa: BLE001
        raise ArtifactUnavailableError("No se pudo cargar el bundle de S4.") from error


def render_bundle_error(st: Any) -> None:
    """Presenta una recuperación segura sin revelar detalles internos."""

    st.error("No se pudo cargar el bundle de S4.")
    st.info("Configura MODEL_UI_BUNDLE y vuelve a ejecutar la aplicación.")


def render_inference_error(st: Any) -> None:
    """Presenta un fallo de validación o inferencia sin detalles sensibles."""

    st.error("No se pudo ejecutar la inferencia.")
    st.info("Revisa los datos y la compatibilidad del bundle de S4.")


def collect_values(st: Any) -> tuple[bool, dict[str, float]]:
    """TODO: renderiza ``FIELD_SPECS`` dentro de un único ``st.form``.

    Cada ``number_input`` debe recibir label, rango, value, step y una key
    estable. Devuelve ``(submitted, values)`` sin llamar al gateway.
    """
    with st.form("wine_quality_form"):
        fixed = st.number_input(
            label="Acidez fija",
            min_value=0.0,
            max_value=20.0,
            value=7.4,
            step=0.1,
            key="input_fixed_acidity",
        )
        volatile = st.number_input(
            label="Acidez volátil",
            min_value=0.0,
            max_value=2.0,
            value=0.7,
            step=0.01,
            key="input_volatile_acidity",
        )
        citric = st.number_input(
            label="Ácido cítrico",
            min_value=0.0,
            max_value=2.0,
            value=0.0,
            step=0.01,
            key="input_citric_acid",
        )
        sugar = st.number_input(
            label="Azúcar residual",
            min_value=0.0,
            max_value=20.0,
            value=1.9,
            step=0.1,
            key="input_residual_sugar",
        )
        chlorides = st.number_input(
            label="Cloruros",
            min_value=0.0,
            max_value=1.0,
            value=0.076,
            step=0.001,
            key="input_chlorides",
        )
        free_sulfur = st.number_input(
            label="Dióxido de azufre libre",
            min_value=0.0,
            max_value=100.0,
            value=11.0,
            step=1.0,
            key="input_free_sulfur_dioxide",
        )
        total_sulfur = st.number_input(
            label="Dióxido de azufre total",
            min_value=0.0,
            max_value=300.0,
            value=34.0,
            step=1.0,
            key="input_total_sulfur_dioxide",
        )

        density = st.number_input(
            label="Densidad",
            min_value=0.98,
            max_value=1.01,
            value=0.9978,
            step=0.0001,
            key="input_density",
        )

        ph = st.number_input(
            label="pH",
            min_value=2.5,
            max_value=4.5,
            value=3.51,
            step=0.01,
            key="input_ph",
        )
        sulphates = st.number_input(
            label="Sulfatos",
            min_value=0.0,
            max_value=3.0,
            value=0.56,
            step=0.01,
            key="input_sulphates",
        )
        alcohol = st.number_input(
            label="Alcohol",
            min_value=5.0,
            max_value=20.0,
            value=9.4,
            step=0.1,
            key="input_alcohol",
        )
        submitted = st.form_submit_button("Ejecutar inferencia")

    data = {
        "fixed_acidity": fixed,
        "volatile_acidity": volatile,
        "citric_acid": citric,
        "residual_sugar": sugar,
        "chlorides": chlorides,
        "free_sulfur_dioxide": free_sulfur,
        "total_sulfur_dioxide": total_sulfur,
        "density": density,
        "ph": ph,
        "sulphates": sulphates,
        "alcohol": alcohol,
    }
    return submitted, data


def render_prediction(st: Any, prediction: PredictionPayload) -> None:
    """TODO: presenta los cuatro campos de ``PredictionPayload``."""

    st.write(f"quality_band: {prediction.quality_band}")
    st.write(f"confidence: {prediction.confidence}")
    st.write(f"model_version: {prediction.model_version}")
    st.write(f"preprocessing_version: {prediction.preprocessing_version}")


def run_app(st: Any, gateway: InferenceGateway) -> None:
    """Conecta submit, gateway y salida sin añadir estado avanzado."""

    submitted, values = collect_values(st)
    if not submitted:
        st.info("Completa el formulario y pulsa «Ejecutar inferencia».")
        return

    try:
        prediction = gateway.predict(values)
    except ArtifactUnavailableError:
        render_bundle_error(st)
        return
    except InputContractError:
        render_inference_error(st)
        return
    except ValueError:
        render_inference_error(st)
        return

    render_prediction(st, prediction)


def run_configured_app(
    st: Any,
    gateway_factory: Callable[[], InferenceGateway] = build_gateway,
) -> None:
    """Carga la configuración y contiene cualquier fallo del bundle."""

    try:
        gateway = gateway_factory()
    except ArtifactUnavailableError:
        render_bundle_error(st)
        return
    run_app(st, gateway)


def main() -> None:
    """Ejecuta la pantalla básica; S6 añadirá estado explícito."""

    try:
        import streamlit as st
    except ModuleNotFoundError as error:
        raise SystemExit(
            "Instala Streamlit con `uv run --with streamlit streamlit run app.py`."
        ) from error

    st.set_page_config(page_title="Wine Quality · S5", page_icon="🍷")
    st.title("Primera interfaz de inferencia")
    st.caption("S5: formulario, gateway y resultado; el estado avanzado llega en S6.")

    run_configured_app(st)


if __name__ == "__main__":
    main()
