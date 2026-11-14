"""S9.4 — Evidencias del contrato: disponibilidad, rangos y OpenAPI."""

import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from wine_api.dependencies import get_predictor
from wine_api.export_openapi import render_openapi
from wine_api.predictor import UnavailablePredictor


def test_prediction_returns_503_when_model_is_unavailable(
    client: TestClient, valid_payload: dict, monkeypatch: pytest.MonkeyPatch
) -> None:
    # Restaura cualquier override previo incluso si falla un assert.
    with monkeypatch.context() as overrides:
        overrides.setitem(
            client.app.dependency_overrides,
            get_predictor,
            lambda: UnavailablePredictor(),
        )
        response = client.post("/v1/predictions", json=valid_payload)

    assert response.status_code == 503
    body = response.json()
    assert body["error"]["code"] == "model_unavailable"
    assert body["request_id"] == response.headers["X-Request-Id"]
    assert "detail" not in body


@pytest.mark.parametrize(
    ("value", "expected_status"),
    [
        pytest.param(4.99, 422, id="below-minimum"),
        pytest.param(20.01, 422, id="above-maximum"),
        pytest.param(None, 422, id="null"),
        pytest.param("not-a-number", 422, id="text"),
        pytest.param(True, 422, id="boolean"),
        pytest.param(5.0, 200, id="inclusive-minimum"),
        pytest.param(20.0, 200, id="inclusive-maximum"),
    ],
)
def test_alcohol_contract(
    client: TestClient, valid_payload: dict, value: object, expected_status: int
) -> None:
    """Rechaza entradas inválidas y acepta ambos límites inclusivos."""
    valid_payload["features"]["alcohol"] = value
    response = client.post("/v1/predictions", json=valid_payload)

    assert response.status_code == expected_status
    body = response.json()
    if expected_status == 422:
        assert body["error"]["code"] == "validation_error"
        assert [item["field"] for item in body["error"]["fields"]] == [
            "features.alcohol"
        ]
    else:
        assert 0 <= body["prediction"]["confidence"] <= 1


def test_openapi_matches_versioned_contract() -> None:
    # Ruta independiente del directorio desde el que se invoque pytest.
    snapshot = Path(__file__).resolve().parents[1] / "contracts" / "openapi.json"
    assert snapshot.is_file(), (
        "Genera el contrato con: uv run python -m wine_api.export_openapi"
    )
    assert json.loads(render_openapi()) == json.loads(
        snapshot.read_text(encoding="utf-8")
    )
