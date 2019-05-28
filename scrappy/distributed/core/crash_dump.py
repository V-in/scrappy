from scrappy import app
from scrappy.core.crash_dump import crash_dump
from flask import jsonify, request
import pydebug

debug = pydebug.debug("distributed:crash_dump")


@app.route("/crash_dump", methods=['POST'])
def crash_dump_route():
    data = request.get_json(force=True)
    try:
        crash_dump(data['caller_id'], data['error'])
        return '', 200
    except Exception as error:
        debug("Error while trying to write crash dump: {}".format(str(error)))
        return '', 400
