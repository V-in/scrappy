class Task():
    def __init__(self, persistor):
        self.persistor = persistor

    def bootstrap_condition(self, driver):
        return True

    def bootstrap(self, driver):
        pass

    def _run(self, driver):
        if(self.bootstrap_condition(driver)):
            self.bootstrap(driver)
        self.run(driver, self.persistor)
