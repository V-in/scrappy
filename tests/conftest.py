import tempfile
import pytest
from scrappy import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    with app.app_context():
        yield client


@pytest.fixture
def coco():
    yield 2
