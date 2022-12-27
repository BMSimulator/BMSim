
class heartbeat_message:
    def __init__(self, source, destination, feature, initTTL, TTL):
        self.heartbeat = 1
        self.friend_update = 0
        self.friend_poll = 0
        self.initTTL = initTTL
        self.TTL = TTL
        self.source = source
        self.destination = destination
        self.source_feature = feature
        self.generation_time = 0
        self.seq_number = 0
