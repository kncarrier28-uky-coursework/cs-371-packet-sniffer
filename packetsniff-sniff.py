from scapy.all import sniff
import pandas as pd
import numpy as np
import sys
import socket
import os
import csv

from packetsniff.flow import Flow
from packetsniff.interfaces import getIpAddresses
from packetsniff.progress import ProgressDisplay


## sniff packets ##
progress = ProgressDisplay("Sniffing packets... ", " processed")

def sniffPacket(x): # remove argument from function call
    progress.next()

flows = []
sniffCount = 1000 # number of packets to sniff
pkts = sniff(filter = "tcp or udp", prn=sniffPacket, count = sniffCount)
#print("\nPackets Sniffed: ", len(pkts))


## detect flows ##
progress.newline()
progress = ProgressDisplay("Calculating flows... ", " processed")

ipaddrs = getIpAddresses()
for pkt in pkts:
    for ip in ipaddrs:
        if (pkt[1].src == ip):
            pkt[1].src = "localhost"
        if (pkt[1].dst == ip):
            pkt[1].dst = "localhost"

    if pkt[1].version == 4:
        inAFlow = False
        for flow in flows:
            if flow.isPartOfFlow(pkt) == True:
                inAFlow = True
        if inAFlow == False:
            flows.append(Flow(pkt))
    #else:
        #print("WARNING: An IPv6 packet was omitted")
    progress.next()


## trim flows ##
# remove flows with <1% of packets
progress.newline()
progress = ProgressDisplay("Trimming flows... "," processed")

flows_orig = list(flows)
for flow in flows_orig:
    if flow.features['numPkts'] < sniffCount*0.01:
        flows.remove(flow)
    progress.next()

progress.newline()
print("Number of Trimmed Flows: ", len(flows))

## write to CSV ##
with open('data/flows.csv', mode='w') as flowInfo:
    flowWriter = csv.writer(flowInfo, delimiter=',', quoting=csv.QUOTE_NONE)
    # write headers
    flowWriter.writerow(["proto", "maxIn", "maxOut", "numPkts", "inSplit", "outSplit"])
    # write flows
    for i, flow in enumerate(flows):
        print("Src IP: ", flow.srcIp, "\nDest IP: ", flow.dstIp, "\n\n")
        flowWriter.writerow([flow.proto, flow.features["maxIn"], flow.features["maxOut"], flow.features["numPkts"], flow.features["inSplit"], flow.features["outSplit"]])
