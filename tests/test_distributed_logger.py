from flask import jsonify
from scrappy import app

client = app.test_client()


def test_distributed_logger():
    assert client.get("/") == jsonify({"key": "Hello World"})
