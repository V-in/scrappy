
from flask import Flask

app = Flask(__name__)

import scrappy.distributed.core.crash_dump

__all__ = ["core", "driver", "persistor",
           "scheduler", "tasks", "util", "distributed"]
