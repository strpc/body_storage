from fastapi.testclient import TestClient


def test_delete_body_wrong_path(http_client: TestClient) -> None:
    response = http_client.delete("/api/body/")

    assert response.status_code == 307


def test_delete_body_not_found(http_client: TestClient) -> None:
    response = http_client.delete("/api/body/foo")

    assert response.status_code == 404


def test_delete_body_success(http_client: TestClient, create_body: str) -> None:
    key = create_body

    response = http_client.delete(f"/api/body/{key}")

    assert response.status_code == 204
    assert key not in http_client.app.state.storage


def test_delete_body_not_found_after_delete(http_client: TestClient, create_body: str) -> None:
    key = create_body

    response = http_client.delete(f"/api/body/{key}")

    assert response.status_code == 204
    assert key not in http_client.app.state.storage

    response = http_client.delete(f"/api/body/{key}")

    assert response.status_code == 404
