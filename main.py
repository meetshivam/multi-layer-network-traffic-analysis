from scapy.all import sniff
from scapy.layers.inet import IP, ICMP

from protocol_classifier import classify_packet
from logger import initialize_logger, log_alert

from detectors.portscan_detector import detect_port_scan
from detectors.dns_detector import detect_dns

from statistics import increment, show_statistics

from layer_statistics import (
    increment_layer,
    show_layer_statistics
)

initialize_logger()


def packet_handler(packet):

    classifications = classify_packet(packet)

    print("\n====================")

    for protocol, layer in classifications:

        print(f"{protocol} --> {layer}")

        # Layer Statistics
        increment_layer(layer)

        # Protocol Statistics

        if protocol == "ARP":
            increment("ARP")

        elif protocol == "IP":
            increment("IP")

        elif protocol == "ICMP":
            increment("ICMP")

        elif protocol == "TCP":
            increment("TCP")

        elif protocol == "UDP":
            increment("UDP")

        elif protocol == "DNS":
            increment("DNS")

    # ICMP Monitoring

    if packet.haslayer(IP) and packet.haslayer(ICMP):

        src_ip = packet[IP].src
        dst_ip = packet[IP].dst

        log_alert(
            "ICMP Traffic",
            src_ip,
            dst_ip,
            "ICMP"
        )

    # Port Scan Detection

    portscan_alert = detect_port_scan(packet)

    if portscan_alert:

        print("\n🚨 PORT SCAN DETECTED 🚨")

        print(
            f"Source IP: {portscan_alert['src_ip']}"
        )

        print(
            f"Ports Scanned: {portscan_alert['dst_port_count']}"
        )

        increment("PortScanAlerts")

        log_alert(
            "Port Scan",
            portscan_alert["src_ip"],
            "N/A",
            "TCP"
        )

    # DNS Monitoring

    dns_alert = detect_dns(packet)

    if dns_alert:

        print("\n🌐 DNS QUERY DETECTED")

        print(
            f"Source IP: {dns_alert['src_ip']}"
        )

        print(
            f"Domain: {dns_alert['domain']}"
        )

        increment("DNSQueries")

        log_alert(
            "DNS Query",
            dns_alert["src_ip"],
            dns_alert["domain"],
            "DNS"
        )


print("\nStarting Multi-Layer Network Traffic Analysis Framework...")
print("Press CTRL + C to stop and generate reports.\n")

try:

    sniff(
        prn=packet_handler,
        store=False
    )

except KeyboardInterrupt:

    print("\nCapture interrupted by user.")

finally:

    print("\nCapture Stopped Successfully.")

    # Protocol Statistics Report
    show_statistics()

    # OSI Layer Statistics Report
    show_layer_statistics()
