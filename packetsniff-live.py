live = True
while(True):
    exec(open('packetsniff-sniff.py').read())
    exec(open('packetsniff-ml.py').read())
    print("\n", end='')