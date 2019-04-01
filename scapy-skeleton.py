from scapy.all import *
import pandas as pd
import numpy as np
import sys
import socket
import os
import csv

def fields_extraction(x):
    print(x.sprintf("{IP:%IP.src%,%IP.dst%,}"
        "{TCP:%TCP.sport%,%TCP.dport%,}"
        "{UDP:%UDP.sport%,%UDP.dport%}"))

    #print x.summary()

    #x.show()
    #use x.time for time information on the pkts
pkts = sniff(prn = fields_extraction, count = 10)

# print pkts[0].show()
with open('flow_info.csv', mode='w') as flow_info:
    flow_writer = csv.writer(flow_info, delimiter=',', quoting=csv.QUOTE_ALL)
    flow_writer.writerow(['flow_id', 'feature_1', 'feature_2', 'feature_3', 'label'])
    # flow_writer.writerow([flow, feature_1_val, feature_2_val, feature_3_val, lab])
