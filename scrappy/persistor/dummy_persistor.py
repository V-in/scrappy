from scrappy.persistor.persistor import Persistor
import pydebug

debug = pydebug.debug("persistor:dummy")


class DummyPersistor():
    def save_one(self, document):
        debug(document.data)
