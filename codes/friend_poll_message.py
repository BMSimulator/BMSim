

class friend_poll_message:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination
        self.heartbeat = 0
        self.friend_poll = 1
        self.friend_update = 0
        self.acknowledge = 0
