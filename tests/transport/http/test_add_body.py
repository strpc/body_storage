from typing import Any

import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize("body", [{}, {"": ""}])
def test_add_body_wrong_body(http_client: TestClient, body: dict[Any, Any]) -> None:
    response = http_client.post("/api/body", json=body)

    assert response.status_code == 422


def test_add_body_success(http_client: TestClient) -> None:
    body = {"foo": "bar"}

    response = http_client.post("/api/body", json=body)

    assert response.status_code == 201
    key = response.json()["key"]
    assert key
    assert key in http_client.app.state.storage
    assert http_client.app.state.storage[key]["duplicates"] == 1


def test_add_body_duplicates_inc_success(http_client: TestClient) -> None:
    body = {"foo": "bar"}

    count = 3
    for i in range(1, count + 1):
        response = http_client.post("/api/body", json=body)

        assert response.status_code == 201
        key = response.json()["key"]
        assert key
        assert key in http_client.app.state.storage
        assert http_client.app.state.storage[key]["duplicates"] == i
