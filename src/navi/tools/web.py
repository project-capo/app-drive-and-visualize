import os
import logging
import threading
import time

from flask import Flask, render_template
from tornado import websocket, ioloop, web


logging.basicConfig()

_pwd = os.path.abspath(__file__)

for i in range(4):
    _pwd = os.path.dirname(_pwd)

_pwd += '/web'

_app_flask = Flask(__name__, template_folder=_pwd)


@_app_flask.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404


@_app_flask.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500


@_app_flask.route('/')
def index():
    return render_template('index.html')


def _run_flask():
    _app_flask.run()


_sockets = []


class WebSocket(websocket.WebSocketHandler):
    def open(self):
        _sockets.append(self)

    def on_close(self):
        _sockets.remove(self)


def _run_tornado():
    application = web.Application([
        (r"/", WebSocket),
    ])
    application.listen(6000)
    ioloop.IOLoop.instance().start()


def emit(data):
    for socket in _sockets:
        socket.write_message(data)


def send(data):
    for socket in _sockets:
        socket.write_message(data)


def start():
    _thread = threading.Thread(target=_run_tornado)
    _thread.start()
    _thread = threading.Thread(target=_run_flask)
    _thread.start()


if __name__ == '__main__':
    start()
    while True:
        emit('data')
        time.sleep(3)