from scapy.layers.dns import DNS, DNSQR
from scapy.layers.inet import IP

def detect_dns(packet):

    if not packet.haslayer(DNS):
        return None

    if not packet.haslayer(DNSQR):
        return None

    if not packet.haslayer(IP):
        return None

    try:

        queried_domain = packet[DNSQR].qname.decode()

        return {
            "src_ip": packet[IP].src,
            "domain": queried_domain
        }

    except:
        return None
