
import random
class message:
    def __init__(self, TTL, source, destination, data):
        self.heartbeat = 0
        self.friend_update = 0
        self.friend_poll = 0
        self.data = data
        self.TTL = TTL
        self.source = source
        self.destination = destination
        self.latency = 0
        self.seq_number = 0
        self.pathlose = random.uniform(0, 1)
        self.generation_time = 0
