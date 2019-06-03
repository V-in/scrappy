class Document(dict):
    def __init__(self, document_id, data):
        """Persistable result of scrapping a web page

        Arguments:
            document_id {any} -- Unique id for this document
            data {any} -- Data that should be persisted
        """
        dict.__init__(self, id=str(document_id), html=data)
        self.id = str(document_id)
        self.data = data
