import json
import matplotlib.pyplot as plt

with open("statistics.json", "r") as file:
    stats = json.load(file)

protocols = [
    "ARP",
    "IP",
    "ICMP",
    "TCP",
    "UDP",
    "DNS"
]

counts = [
    stats["ARP"],
    stats["IP"],
    stats["ICMP"],
    stats["TCP"],
    stats["UDP"],
    stats["DNS"]
]

plt.figure(figsize=(8, 5))

plt.bar(protocols, counts)

plt.title("Protocol Distribution Analysis")

plt.xlabel("Protocol")

plt.ylabel("Packet Count")

plt.tight_layout()

plt.savefig("protocol_distribution.png")

print("Protocol graph generated successfully.")
