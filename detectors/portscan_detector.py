from scapy.layers.inet import IP, TCP

scan_tracker = {}
alerted_hosts = set()

PORT_THRESHOLD = 10

def detect_port_scan(packet):

    if not packet.haslayer(IP):
        return None

    if not packet.haslayer(TCP):
        return None

    src_ip = packet[IP].src
    dst_port = packet[TCP].dport

    if src_ip not in scan_tracker:
        scan_tracker[src_ip] = set()

    scan_tracker[src_ip].add(dst_port)

    if (
        len(scan_tracker[src_ip]) >= PORT_THRESHOLD
        and src_ip not in alerted_hosts
    ):

        alerted_hosts.add(src_ip)

        return {
            "alert": "Possible Port Scan",
            "src_ip": src_ip,
            "dst_port_count": len(scan_tracker[src_ip])
        }

    return None
