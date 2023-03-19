import uuid
from tcpsender import TCPSender

class Observer:
    def __init__(self, id=None, sender=None, port=9000, host="localhost") -> None:
        if (id is None):
            id = uuid.uuid1()
        self._id = id
        if (sender is None):
           sender = TCPSender(port, host)
        self._sender = sender

    def set_sender(self, sender):
        self._sender = sender

    async def update(self, state, source):
        if (source == self._id):
            return
        return await self._sender.send_data(self.prepare_data(state))

    def prepare_data(self, data):
        data["source"] = str(self._id)
        return data