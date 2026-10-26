from scapy.all import sniff, wrpcap

print("Capturing 50 packets...")

packets = sniff(count=50)

wrpcap("test_capture.pcap", packets)

print("PCAP saved successfully.")
