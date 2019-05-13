from scrappy.tasks.task import Task


class SimpleTask(Task):
    def __init__(self, persistor):
        Task.__init__(self, persistor)

    def run(self, driver, persistor):
        raise NotImplementedError
