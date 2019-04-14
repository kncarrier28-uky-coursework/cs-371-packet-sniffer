from scapy.all import sniff
import pandas as pd
import numpy as np
import sys
import socket
import os
import csv
import statistics

# with open('pkt_info.csv', mode='w') as pkt_info:
#    pkt_writer = csv.writer(pkt_info, delimiter=',', quoting=csv.QUOTE_ALL)
#    pkts = sniff(prn = fields_extraction, count = 10)

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

# progress display
progressCount = 0 # number processed
def progressPrint():
    global progressCount
    message = " processed" # appended after count

    # erase packet count + message
    for x in range(0, len(str(progressCount)) + len(message)):
        print("\b", end='')

    progressCount += 1

    # print count + message
    print(str(progressCount) + message, end='')

# print initial progress message
print("Sniffing packets... 0 processed", end='')

def sniffProgress(x): # remove argument from function call
    progressPrint()

# sniff packets
flows = []
sniffCount = 2000 # number of packets to sniff
pkts = sniff(filter = "tcp or udp", prn=sniffProgress, count = sniffCount)
#print("\nPackets Sniffed: ", len(pkts))

# detect flows
progressCount = 0
print("\nCalculating flows... 0 processed", end='')

for pkt in pkts:
    if pkt[1].version == 4:
        inAFlow = False
        for flow in flows:
            if flow.isPartOfFlow(pkt) == True:
                inAFlow = True
        if inAFlow == False:
            flows.append(Flow(pkt))
    #else:
        #print("WARNING: An IPv6 packet was omitted")
    progressPrint()

#print("\n", end='')
#print("Number of Detected Flows: ", len(flows))

# remove flows with <1% of packets
progressCount = 0
print("\n", end='')
print("Trimming flows... 0 processed", end='')

flows_orig = list(flows)
for flow in flows_orig:
    if flow.numPkts < sniffCount*0.01:
        flows.remove(flow)
    progressPrint()

print("\n", end='')
print("Number of Trimmed Flows: ", len(flows))

# write to CSV
with open('flow_info.csv', mode='w') as flowInfo:
    flowWriter = csv.writer(flowInfo, delimiter=',', quoting=csv.QUOTE_NONE)
    # write headers
    flowWriter.writerow(["proto", "avgSize", "avgTtl", "numPkts", "avgAckTime", "type"])
    # write flows
    for i, flow in enumerate(flows):
        flowDump = flow.dump()
        flowWriter.writerow([flowDump[0], flowDump[1], flowDump[2], flowDump[3], flowDump[4], 1])
