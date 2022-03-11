from typing import Any

import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize("body", [{}, {"": ""}])
def test_update_body_wrong_body(http_client: TestClient, body: dict[Any, Any]) -> None:
    response = http_client.put("/api/body/foo", json=body)

    assert response.status_code == 422


def test_update_body_not_found(http_client: TestClient) -> None:
    body = {"foo": "bar"}

    response = http_client.put("/api/body/foo", json=body)

    assert response.status_code == 404


def test_update_body_success(http_client: TestClient, create_body: str) -> None:
    new_body: dict[str, Any] = {"foo": "baz"}
    key = create_body

    response = http_client.put(f"/api/body/{key}", json=new_body)

    assert response.status_code == 200
    key = response.json()["key"]
    assert key
    assert key in http_client.app.state.storage

    new_body["duplicates"] = 1
    assert http_client.app.state.storage[key] == new_body


def test_update_body_success_reset_duplicates(http_client: TestClient, create_body: str) -> None:
    key = create_body
    http_client.app.state.storage[key]["duplicates"] = 500

    new_body: dict[str, Any] = {"foo": "baz"}

    response = http_client.put(f"/api/body/{key}", json=new_body)

    assert response.status_code == 200
    key = response.json()["key"]
    assert key
    assert key in http_client.app.state.storage

    new_body["duplicates"] = 1
    assert http_client.app.state.storage[key] == new_body
