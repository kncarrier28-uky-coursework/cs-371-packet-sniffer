from scapy.all import sniff
import pandas as pd
import numpy as np
import sys
import socket
import os
import csv

from packetsniff.flow import Flow

## progress display ##
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


## sniff packets ##
# print initial progress message
print("Sniffing packets... 0 processed", end='')

def sniffProgress(x): # remove argument from function call
    progressPrint()

flows = []
sniffCount = 2000 # number of packets to sniff
pkts = sniff(filter = "tcp or udp", prn=sniffProgress, count = sniffCount)
#print("\nPackets Sniffed: ", len(pkts))


## detect flows ##
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


## trim flows ##
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


## write to CSV ##
with open('flow_info.csv', mode='w') as flowInfo:
    flowWriter = csv.writer(flowInfo, delimiter=',', quoting=csv.QUOTE_NONE)
    # write headers
    flowWriter.writerow(["proto", "avgSize", "avgTtl", "numPkts", "avgAckTime", "type"])
    # write flows
    for i, flow in enumerate(flows):
        flowDump = flow.dump()
        flowWriter.writerow([flowDump[0], flowDump[1], flowDump[2], flowDump[3], flowDump[4], 1])
