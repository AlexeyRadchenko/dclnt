import redis


class TaskQueue:
    def __init__(self, name, namespace='queue', **redis_kwargs):
        self.db_conn = redis.Redis(**redis_kwargs)
        self.key = '%s:%s' % (namespace, name)

    def qsize(self):
        """Return the approximate size of the queue."""
        return self.db_conn.llen(self.key)

    def empty(self):
        """Return True if the queue is empty, False otherwise."""
        return self.qsize() == 0

    def put(self, item):
        """Put item into the queue."""
        self.db_conn.rpush(self.key, item)

    def get(self, block=True, timeout=None):
        """Remove and return an item from the queue. 
    
        If optional args block is true and timeout is None (the default), block
        if necessary until an item is available."""
        if block:
            item = self.db_conn.blpop(self.key, timeout=timeout)
        else:
            item = self.db_conn.lpop(self.key)

        if item:
            item = item[1]
        return item

    def get_nowait(self):
        """Equivalent to get(False)."""
        return self.get(False)
