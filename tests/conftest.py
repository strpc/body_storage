from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.main import HTTPApp


@pytest.fixture()
def app() -> FastAPI:
    return HTTPApp.create_app()


@pytest.fixture()
def http_client(
    app: FastAPI,
) -> Generator[TestClient, None, None]:
    with TestClient(
        app=app,
        base_url="http://test",
    ) as client:
        yield client


@pytest.fixture()
def create_body(http_client: TestClient) -> Generator[str, None, None]:
    key = "foo"
    storage = {key: {"foo": "bar", "duplicates": 1}}
    http_client.app.state.storage = storage

    yield key

    http_client.app.state.storage = {}
