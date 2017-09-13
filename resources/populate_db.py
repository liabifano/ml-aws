import os
import json
import sys
import asyncio
import requests
import logging

REQUESTS_FOLDER = os.path.join(os.path.abspath(os.path.join(__file__, '../')), 'json-requests')

def make_request(i, endpoint):
    file_path = os.path.join(REQUESTS_FOLDER, 'request_{}.json'.format(i))
    with open(file_path, 'r') as f:
        data = json.load(f)
    requests.post('http://{}'.format(endpoint), json=data)


async def make_requests(endpoint, n):
    loop = asyncio.get_event_loop()
    futures = [
        loop.run_in_executor(
            None,
            make_request,
            i,
            endpoint
        )
        for i in range(n)
    ]
    for response in await asyncio.gather(*futures):
        pass


if __name__ == '__main__':
    endpoint = 'localhost:80/run/' if len(sys.argv) == 1 else sys.argv[1]
    logging.warning('Endpoint: {}'.format(endpoint))
    n_requests = len([f for f in os.listdir(REQUESTS_FOLDER)
                      if os.path.isfile(os.path.join(REQUESTS_FOLDER, f))])
    loop = asyncio.get_event_loop()
    loop.run_until_complete(make_requests(endpoint, n_requests))
