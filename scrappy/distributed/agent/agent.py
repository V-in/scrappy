from scrappy.scheduler.round_robin import RoundRobin


class Agent():
    def __init__(self, pool_size, nick_name):
        self.pool_size = pool_size
        self.nick_name = nick_name
