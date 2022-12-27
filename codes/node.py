
import numpy as np
import random
class node:
    def __init__(self, ID, Xposition=0, Yposition=9):
        self.ID = ID
        self.Xposition = Xposition
        self.Yposition = Yposition
        self.GENERATION_INTERVAL = 1000
        self.Advertise_Interval = 20
        self.Relay_Retransmission_Interval = 20
        self.Transmission_Interval = 20
        self.SCAN_WINDOW = 30
        self.SCAN_INTERVAL = 30
        self.Relay_Retransmit_Count = 0
        self.Network_Transmit_Count = 0
        self.Rris = 1
        self.Ntis = 1
        self.NODE_RANGE = 10
        self.unicastaddress = 1
        self.groupaddress = 0
        self.last_seq_number = np.full(50, 0)
        self.friend_queue = []
        self.last_poll_time = 0
        self.response_friend_time = 50000
        self.LOW_POWER_ID = -1
        self.friend_Id = -1
        self.previous_ack = 1
        self.not_receive = 0
        self.Low_Scan_Time = 0
        self.low_power_ack = 0
        self.feature = 6
        self.cache = []
        self.five_hop = []
        self.buffer = []
        self.keynet = []
        self.channel37 = 0
        self.channel38 = 0
        self.channel39 = 0
        self.advertisetag37 = 0  # these flags are used for collision detection
        self.advertisetag38 = 0
        self.advertisetag39 = 0
        self.neighbors = []
        self.message = 0
        self.L_scan = 8
        self.init_time = 0
        self.first_time_scan = 0
        self.last_T_relay = random.randint(0, 30)  # Initial random value
        self.last_T_generation = random.randint(0, 30)
        self.last_t_scan = random.randint(0, 50)
        self.h_last_seq_number = np.full(50, 0)
        self.node_TTL = 0
        self.time_heartbeat = random.randint(0, 1000)
        self.seq_number = 0
        self.h_seq_number = 0
        self.Gen_cache = []
        self.heart_cache = []
        self.Sleep_Time = 0
        self.Scan_Time = 0
        self.Switch_Time = 0
        self.Transmit_Time = 0
        self.minhop = 127
        self.maxhop = 0
        self.Heartbeat_period = 0
        self.n_count = 0
        self.r_count = 0
        self.last_relay_time = random.randint(0, 120)  # Initial random value
        self.last_generation_time = random.randint(0, 1000)

    def scanchannel37(self, ch1):
        self.cache.append(ch1)

    def scanchannel38(self, ch2):
        self.cache.append(ch2)

    def scanchannel39(self, ch3):
        self.cache.append(ch3)

    def advertising_37(self, message):
        self.channel37 = message

    def advertising_38(self, message):
        self.channel38 = message

    def advertising_39(self, message):
        self.channel39 = message
