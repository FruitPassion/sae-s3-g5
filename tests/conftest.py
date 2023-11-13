import pytest
import os, sys

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app import create_app


@pytest.fixture()
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
    })

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()

