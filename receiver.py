import time
from datetime import datetime

import requests


def print_messages(messages):
    for message in messages:
        dt = datetime.fromtimestamp(message['time'])
        dt = dt.strftime('%H:%M')
        print(dt, message['name'])
        print(message['text'])
        print()


after = 0

while True:
    response = requests.get(
        'http://127.0.0.1:5000/messages',
        params={'after': after}
    )
    messages = response.json()['messages']
    if len(messages) > 0:
        print_messages(messages)
        after = messages[-1]['time']

    time.sleep(1)
