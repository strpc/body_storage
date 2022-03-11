from typing import Any

import pytest
from fastapi.testclient import TestClient


def test_get_stats_without_data(http_client: TestClient) -> None:
    response = http_client.get("/api/statistic")

    assert response.status_code == 200
    assert response.json()["percent_duplicates"] == 0


@pytest.mark.parametrize(
    "storage, percent_duplicates",
    [
        ({"foo": {"duplicates": 20}, "bar": {"duplicates": 1}}, 950),
        ({"foo": {"duplicates": 1}, "bar": {"duplicates": 1}}, 0),
        (
            {
                "foo": {"duplicates": 2},
                "bar": {"duplicates": 1},
                "baz": {"duplicates": 1},
                "lorem": {"duplicates": 1},
            },
            25,
        ),
    ],
)
def test_get_stats_with_data(
    http_client: TestClient,
    storage: dict[Any, Any],
    percent_duplicates: int,
) -> None:
    http_client.app.state.storage = storage

    response = http_client.get("/api/statistic")

    assert response.status_code == 200
    assert response.json()["percent_duplicates"] == percent_duplicates
