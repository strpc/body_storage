from typing import Any

import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize("params", [{}, {"key": None}])
def test_get_body_wrong_query(http_client: TestClient, params: dict[Any, Any]) -> None:
    response = http_client.get("/api/body", params=params)

    assert response.status_code == 422


@pytest.mark.parametrize(
    "key",
    [
        "foo",
        "",
    ],
)
def test_get_body_not_found(http_client: TestClient, key: str) -> None:
    response = http_client.get("/api/body", params={"key": key})

    assert response.status_code == 404


def test_get_body_success(create_body: str, http_client: TestClient) -> None:
    key = create_body

    response = http_client.get("/api/body", params={"key": key})

    assert response.status_code == 200
    assert response.json()
