import statistics

class Flow:
    def __init__(self, pkt):
        self.ipVersion = pkt[1].version
        if self.ipVersion == 6:
            self.proto = pkt[1].nh
        else:
            self.proto = pkt[1].proto
        self.avgAckTime = -1
        if self.proto == 6:
            self.avgAckTime = 0
        self.srcIp = pkt[1].src
        self.dstIp = pkt[1].dst
        self.srcPort = pkt[2].sport
        self.dstPort = pkt[2].dport
        self.avgSize = pkt[1].len
        self.avgTtl = pkt[1].ttl
        self.pkts = [pkt]
        self.numPkts = 1

    def isPartOfFlow(self, pkt):
        pktProto = pkt[1].proto if pkt[1].version == 4 else pkt[1].nh
        if pktProto == self.proto:
            if (pkt[1].src == self.srcIp and pkt[1].dst == self.dstIp) or (pkt[1].src == self.dstIp and pkt[1].dst == self.srcIp):
                if (pkt[1].sport == self.srcPort and pkt[1].dport == self.dstPort) or (pkt[1].sport == self.dstPort and pkt[1].dport == self.srcPort):
                    self.calcFeatures(pkt)
                    if self.proto == 6:
                        self.checkForAck(pkt)
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

    def checkForAck(self, pkt):
        for flowPkt in self.pkts:
            if flowPkt[2].seq == pkt[2].ack:
                if self.avgAckTime == -1 or self.avgAckTime == 0:
                    self.avgAckTime = pkt.time - flowPkt.time
                else:
                    self.avgAckTime = statistics.mean([pkt.time - flowPkt.time, self.avgAckTime])
                self.pkts.pop(self.pkts.index(flowPkt))

    def printFeatures(self):
        print("Number of Packets in flow: ", self.numPkts)
        print("Average size of packets: ", self.avgSize)
        print("Average time to live of packets: ", self.avgTtl)
        print("Protocol used: ", self.proto)
        if self.proto == 6:
            if self.avgAckTime == -1:
                print("No acks received, try sniffing more packets")
            else:
                print("Average time to ack: ", self.avgAckTime, " seconds")

    def dump(self):
        return [self.proto, self.avgSize, self.avgTtl, self.numPkts, self.avgAckTime]

# live printout of packets
#def fields_extraction(x):
#    print(x.sprintf("{IP:%IP.src%, %IP.dst%, %IP.len%, }"
#        "{IPv6:%IPv6.src%, %IPv6.dst%, %IPv6.plen%, }"
#        "{TCP:%TCP.sport%, %TCP.dport%}"
#        "{UDP:%UDP.sport%, %UDP.dport%}"))
