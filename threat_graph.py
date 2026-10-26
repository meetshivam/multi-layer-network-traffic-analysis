import json
import matplotlib.pyplot as plt

with open("statistics.json", "r") as file:
    stats = json.load(file)

threats = [
    "DNS Queries",
    "Port Scan Alerts"
]

values = [
    stats["DNSQueries"],
    stats["PortScanAlerts"]
]

plt.figure(figsize=(7, 5))

plt.bar(threats, values)

plt.title("Threat Detection Events")

plt.xlabel("Threat Type")
plt.ylabel("Number of Events")

plt.tight_layout()

plt.savefig("threat_detection.png")

print("Threat detection graph generated successfully.")
