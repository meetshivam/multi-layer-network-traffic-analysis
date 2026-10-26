from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.dns import DNS
from scapy.layers.l2 import ARP

def classify_packet(packet):

    protocols = []

    if packet.haslayer(ARP):
        protocols.append(("ARP", "Data Link Layer"))

    if packet.haslayer(IP):
        protocols.append(("IP", "Network Layer"))

    if packet.haslayer(ICMP):
        protocols.append(("ICMP", "Network Layer"))

    if packet.haslayer(TCP):
        protocols.append(("TCP", "Transport Layer"))

        sport = packet[TCP].sport
        dport = packet[TCP].dport

        if sport == 22 or dport == 22:
            protocols.append(("SSH", "Application Layer"))

        if sport == 80 or dport == 80:
            protocols.append(("HTTP", "Application Layer"))

        if sport == 443 or dport == 443:
            protocols.append(("HTTPS", "Application Layer"))

    if packet.haslayer(UDP):
        protocols.append(("UDP", "Transport Layer"))

    if packet.haslayer(DNS):
        protocols.append(("DNS", "Application Layer"))

    return protocols
