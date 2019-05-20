from scrappy.persistor.in_memory import InMemoryPersistor
from scrappy.persistor.document import Document


def test_in_memory_persistor():
    p = InMemoryPersistor()
    doc = Document(1, "vinicius misael")
    p.save_one(doc)
    assert(len(p.data) == 1)
    assert(p.data[0] == doc)
