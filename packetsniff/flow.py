import statistics

class Flow:
    def __init__(self, pkt):
        self.ipVersion = pkt[1].version
        self.proto = pkt[1].proto
        self.srcIp = pkt[1].src if pkt[1].src == 'localhost' else pkt[1].dst
        self.dstIp = pkt[1].dst if pkt[1].src == 'localhost' else pkt[1].src
        self.srcPort = pkt[2].sport if pkt[1].src == 'localhost' else pkt[2].dport
        self.dstPort = pkt[2].dport if pkt[1].src == 'localhost' else pkt[2].sport
        self.features = {
            'numPkts': 1,
            'maxIn': pkt[1].len if pkt[1].dst == 'localhost' else 0,
            'maxOut': pkt[1].len if pkt[1].src == 'localhost' else 0,
            'inSplit': 1 if pkt[1].dst == 'localhost' else 0,
            'outSplit': 1 if pkt[1].src == 'localhost' else 0
        }
        self.pkts = [pkt]

    def isPartOfFlow(self, pkt):
        pktProto = pkt[1].proto
        if pktProto == self.proto:
            if (pkt[1].src == self.srcIp and pkt[1].dst == self.dstIp) or (pkt[1].src == self.dstIp and pkt[1].dst == self.srcIp):
                if (pkt[1].sport == self.srcPort and pkt[1].dport == self.dstPort) or (pkt[1].sport == self.dstPort and pkt[1].dport == self.srcPort):
                    self.features['numPkts'] += 1
                    self.calcFeatures(pkt)
                    self.pkts.append(pkt)
                    return True
        return False

    def calcFeatures(self, pkt):
        self.trafficSplit(pkt)
        self.maxPacketSize(pkt)

    def trafficSplit(self, pkt):
        key = 'outSplit' if pkt[1].src == 'localhost' else 'inSplit'
        otherKey = 'inSplit' if pkt[1].src == 'localhost' else 'outSplit'
        self.features[key] = ((self.features[key] * (self.features['numPkts'] - 1)) + 1) / self.features['numPkts']
        self.features[otherKey] = 1 - self.features[key]

    def maxPacketSize(self, pkt):
        key = 'maxOut' if pkt[1].src == 'localhost' else 'maxIn'
        if self.features[key] < pkt[1].len:
            self.features[key] = pkt[1].len

    def printFeatures(self):
        print("Number of Packets in flow: ", self.features['numPkts'])
        print("Protocol used: ", self.proto)

# live printout of packets
#def fields_extraction(x):
#    print(x.sprintf("{IP:%IP.src%, %IP.dst%, %IP.len%, }"
#        "{IPv6:%IPv6.src%, %IPv6.dst%, %IPv6.plen%, }"
#        "{TCP:%TCP.sport%, %TCP.dport%}"
#        "{UDP:%UDP.sport%, %UDP.dport%}"))
