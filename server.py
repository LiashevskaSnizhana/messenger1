import time
from datetime import datetime

from flask import Flask, request, abort

app = Flask(__name__)
db = [
    {
        'name': 'Nick',
        'text': 'Hello!',
        'time': 0.1
    },
    {
        'name': 'Ivan',
        'text': 'Hello, Nick!',
        'time': 0.2
    },
]


@app.route("/")
def hello():
    return "Hello, Messenger!"


@app.route("/status")
def status():
    dt = datetime.now()
    return {
        'status': True,
        'name': 'Skillbox Messenger',  # произвольное имя вашего мессенджера
        'time': time.time(),  # текущее время на сервере
        'time2': time.asctime(),
        'time3': dt,
        'time4': str(dt),
        'time5': dt.isoformat(),
        'time6': dt.strftime('%Y/%m/%d %H:%M')
    }


@app.route("/send", methods=['POST'])
def send_message():
    data = request.json

    if not isinstance(data, dict):
        return abort(400)
    if 'name' not in data or 'text' not in data:
        return abort(400)

    name = data['name']
    text = data['text']

    if not isinstance(name, str) or not isinstance(text, str):
        return abort(400)
    if name == '' or text == '':
        return abort(400)

    db.append({
        'name': name,
        'text': text,
        'time': time.time()
    })

    return {'ok': True}


@app.route("/messages")
def get_messages():
    try:
        after = float(request.args['after'])
    except:
        return abort(400)

    messages = []
    for message in db:
        if message['time'] > after:
            messages.append(message)

    return {'messages': messages[:50]}


app.run()
