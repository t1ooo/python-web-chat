from collections import deque
from flask import Flask
from flask import render_template
from flask_socketio import SocketIO, emit


class History:
    def append(self, item):
        raise NotImplementedError()

    def to_list(self):
        raise NotImplementedError()


class InMemoryHistory(History):
    def __init__(self, messages=[], maxsize=10):
        self.queue = deque(messages, maxsize)

    def append(self, item):
        self.queue.append(item)

    def to_list(self):
        return list(self.queue)


app = Flask(__name__, template_folder="", static_folder="")
app.config["TEMPLATES_AUTO_RELOAD"] = True

socketio = SocketIO(app)

history = InMemoryHistory(
    [
        {"date": "2023-10-13T10:24:05.045Z", "message": "Hello!"},
        {"date": "2023-10-13T10:24:06.045Z", "message": "Hi"},
        {"date": "2023-10-13T10:24:07.045Z", "message": "How are you?"},
    ]
)


@app.route("/")
def main():
    return render_template("app.html")


@socketio.on("connect")
def handle_new_user(data):
    print(f"received message: {data}")
    emit("messages", history.to_list())


@socketio.on("message")
def handle_message(data):
    print(f"received message: {data}")
    history.append(data)
    emit("message", data, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, use_reloader=True, log_output=True)
