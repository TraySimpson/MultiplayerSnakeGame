import uuid
from tcpsender import TCPSender

class Observer:
    def __init__(self) -> None:
        self._id = uuid.uuid1()
        self._sender = TCPSender()

    def update(self, state):
        self._sender.send_data(self.prepare_data(state))

    def prepare_data(self, data):
        data["source"] = self._id
        return data