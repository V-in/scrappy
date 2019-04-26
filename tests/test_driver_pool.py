from scrappy.driver.pool import create, start_all, dispose


def test_pool_lifecycle():
    # Birth
    pool = create(5)
    for worker in pool:
        assert not worker.is_open

    # Life
    start_all(pool)
    for worker in pool:
        assert worker.is_open

    # Death
    dispose(pool)
