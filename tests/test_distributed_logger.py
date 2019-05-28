from flask import jsonify
from scrappy import app
import json
import pytest


def test_distributed_crash_dump(client):
    data = {
        "caller_id": 1,
        "error": "Error"
    }
    res = client.post(
        "/crash_dump",
        data=json.dumps(data),
    )
    assert res.status_code == 200


def test_distributed_crash_dump_bad_data(client):
    data = {
        "caller_id": 1,
    }
    res = client.post(
        "/crash_dump",
        data=json.dumps(data),
    )
    assert res.status_code == 400
