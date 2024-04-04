import tempfile

import pytest
import os
import sys
from sqlalchemy import create_engine

sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from app import create_app


@pytest.fixture()
def app():
    app = create_app('test')

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()