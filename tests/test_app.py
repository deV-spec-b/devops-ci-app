"""Модульные тесты HTTP-приложения."""

import os
import sys

import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.app import create_app


@pytest.fixture(name="test_client")
def fixture_client():
    """Создаёт клиент Flask для запросов к приложению."""
    application = create_app()
    application.config["TESTING"] = True
    with application.test_client() as client:
        yield client


def test_health(test_client):
    """Проверяет ответ проверки жизнеспособности."""
    response = test_client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_index(test_client):
    """Проверяет сведения о службе."""
    response = test_client.get("/")
    data = response.get_json()
    assert response.status_code == 200
    assert data["service"] == "devops-ci-app"
    assert data["status"] == "running"
