import statistics

class Flow:
    def __init__(self, pkt):
        self.ipVersion = pkt[1].version
        self.proto = pkt[1].proto
        self.srcIp = pkt[1].src
        self.dstIp = pkt[1].dst
        self.srcPort = pkt[2].sport
        self.dstPort = pkt[2].dport
        if pkt[1].dst == 'localhost':
            self.srcIp = pkt[1].dst
            self.dstIp = pkt[1].src
            self.srcPort = pkt[2].dport
            self.dstPort = pkt[2].sport
        self.avgSize = pkt[1].len
        self.avgTtl = pkt[1].ttl
        self.pkts = [pkt]
        self.numPkts = 1

    def isPartOfFlow(self, pkt):
        pktProto = pkt[1].proto
        if pktProto == self.proto:
            if (pkt[1].src == self.srcIp and pkt[1].dst == self.dstIp) or (pkt[1].src == self.dstIp and pkt[1].dst == self.srcIp):
                if (pkt[1].sport == self.srcPort and pkt[1].dport == self.dstPort) or (pkt[1].sport == self.dstPort and pkt[1].dport == self.srcPort):
                    self.calcFeatures(pkt)
                    self.pkts.append(pkt)
                    self.numPkts += 1
                    return True
        return False

    def calcFeatures(self, pkt):
        self.calcAvgSize(pkt)
        self.calcAvgTtl(pkt)

    def calcAvgSize(self, pkt):
        self.avgSize = statistics.mean([self.avgSize, pkt[1].len])

    def calcAvgTtl(self, pkt):
        self.avgTtl = statistics.mean([self.avgTtl, pkt[1].ttl])

    def printFeatures(self):
        print("Number of Packets in flow: ", self.numPkts)
        print("Average size of packets: ", self.avgSize)
        print("Average time to live of packets: ", self.avgTtl)
        print("Protocol used: ", self.proto)

# live printout of packets
#def fields_extraction(x):
#    print(x.sprintf("{IP:%IP.src%, %IP.dst%, %IP.len%, }"
#        "{IPv6:%IPv6.src%, %IPv6.dst%, %IPv6.plen%, }"
#        "{TCP:%TCP.sport%, %TCP.dport%}"
#        "{UDP:%UDP.sport%, %UDP.dport%}"))
