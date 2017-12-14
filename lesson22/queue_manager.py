import json
from time import sleep

import redis


class Client:
    prefix = 'qm_task_queue_'

    def __init__(self, redis_connection_params, tasks):
        self.tasks = tasks
        self.redis_client = redis.StrictRedis(**redis_connection_params)

    def enqueue(self, task_name, tasks_kwargs):
        task_info = {
            'task_name': task_name,
            'tasks_kwargs': tasks_kwargs,
        }
        payload = json.dumps(task_info)
        queue_name = '%s%s' % (self.prefix, task_name)
        self.redis_client.lpush(queue_name, payload)

    def start_worker(self):
        queue_name = '%s%s' % (self.prefix, list(self.tasks.keys())[0])
        while True:
            raw_tasks_info = self.redis_client.blpop(queue_name)
            print('Start processing item %s' % str(raw_tasks_info))
            task_info = json.loads(raw_tasks_info[1].decode('utf-8'))
            task_callable = self.tasks[task_info['task_name']]
            task_callable(**task_info['tasks_kwargs'])
            print('Processing task %s with kwargs %s' % (
                task_info['task_name'],
                task_info['tasks_kwargs'],
            ))
            print('\tfinished')


if __name__ == '__main__':
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    r.set('foo', 'bar')
    print(r.get('foo'))