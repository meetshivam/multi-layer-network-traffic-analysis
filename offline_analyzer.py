from scapy.all import rdpcap

from protocol_classifier import classify_packet

pcap_file = "test_capture.pcap"

packets = rdpcap(pcap_file)

print("\nOffline PCAP Analysis Started...\n")

packet_count = 0

for packet in packets:

    packet_count += 1

    print(f"\nPacket #{packet_count}")

    classifications = classify_packet(packet)

    for protocol, layer in classifications:

        print(f"{protocol} --> {layer}")

print("\nAnalysis Completed.")
print(f"Total Packets: {packet_count}")
