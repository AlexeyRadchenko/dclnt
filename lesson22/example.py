import requests

import lesson22.queue_manager as qm


def fetch_url(url):
    print(len(requests.get(url).text))


def get_queue_manager():
    return qm.Client(
        redis_connection_params={
            'host': 'localhost',
            'port': 6379,
            'db': 0
        },
        tasks={
            'fetch_url': fetch_url,
        },
    )

if __name__ == '__main__':
    queue_client = qm.Client(
        redis_connection_params={
            'host': 'localhost',
            'port': 6379,
            'db': 0
        },
        tasks={
            'fetch_url': fetch_url,
        },
    )

    urls = [
        'https://google.com',
        'https://yandex.ru',
        'https://vk.com',
    ]
    for url in urls:
        queue_client.enqueue('fetch_url', {'url': url})