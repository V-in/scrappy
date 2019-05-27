from scrappy import app
from scrappy.core import crash_dump
from flask import jsonify, request


@app.route("/workers/<worker_id>/logs")
def worker_log(worker_id):
    return "QWEQWEK"


@app.route("/nodes/<node_id>/logs")
def node_log(node_id):
    return jsonify({
        "id": node_id
    })


@app.route("/crash_dump/", )
def crash_dump():
    return jsonify({
        "id": request.args.get("worker_id")
    })
