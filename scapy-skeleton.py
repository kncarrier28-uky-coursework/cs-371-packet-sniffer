from scapy.all import *
import pandas as pd
import numpy as np
import sys
import socket
import os
import csv

class Flow:
    def __init__(self, pkt):
        self.proto = pkt[1].proto
        self.srcIp = pkt[1].src
        self.dstIp = pkt[1].dst
        self.srcPort = pkt[2].sport
        self.dstPort = pkt[2].dport

    def isPartOfFlow(self, pkt):
        isInFlow = False
        if pkt[1].proto == self.proto:
            isInFlow = (pkt[1].src == self.srcIp and pkt[1].dst == self.dstIp) or (pkt[1].src == self.dstIp and pkt[1].dst == self.srcIp)
            if isInFlow:
                isInFlow = (pkt[1].sport == self.srcPort and pkt[1].dport == self.dstPort) or (pkt[1].sport == self.dstPort and pkt[1].dport == self.srcPort)
        return isInFlow

    def calculateFeatures():
        print("test")

def fields_extraction(x):
    print(x.sprintf("{IP:%IP.src%, %IP.dst%, }"
            "{TCP:%TCP.sport%, %TCP.dport%, }"
            "{UDP:%UDP.sport%, %UDP.dport%}"))

flows = []

pkts = sniff(filter = "tcp or udp", prn = fields_extraction, count = 1000)

print("\nPackets Sniffed: ", len(pkts))

flows.append(Flow(pkts[0]))
pkts.pop(0)

for pkt in pkts:
    inAFlow = False
    for flow in flows:
        if flow.isPartOfFlow(pkt) == True:
            inAFlow = True
    if inAFlow == False:
        flows.append(Flow(pkt))

print("Number of Detected Flows: ", len(flows))
