

class friend_update:
    def __init__(self, source, destination):
        self.friend_poll = 1
        self.heartbeat = 0
        self.friend_update = 0
        self.source = source
        self.destination = destination
