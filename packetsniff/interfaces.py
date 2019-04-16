import netifaces

def getIpAddresses():
    ipaddrs = []
    for interface in netifaces.interfaces():
        if netifaces.AF_INET in netifaces.ifaddresses(interface):
            for address in netifaces.ifaddresses(interface)[netifaces.AF_INET]:
                if 'addr' in address:
                    ipaddrs.append(address['addr'])
    return ipaddrs