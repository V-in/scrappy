class Task():
    def __init__(self, persistor, extra_args=None):
        self.persistor = persistor
        self.extra_args = extra_args

    def bootstrap_condition(self, driver):
        return True

    def bootstrap(self, driver):
        pass

    def _run(self, driver):
        if(self.bootstrap_condition(driver)):
            self.bootstrap(driver)
        self.run(driver, self.persistor)
