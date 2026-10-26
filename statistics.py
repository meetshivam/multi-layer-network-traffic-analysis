import json

stats = {

    "ARP": 0,
    "IP": 0,
    "ICMP": 0,
    "TCP": 0,
    "UDP": 0,
    "DNS": 0,

    "PortScanAlerts": 0,
    "DNSQueries": 0
}


def increment(counter):

    if counter in stats:
        stats[counter] += 1


def save_statistics():

    with open("statistics.json", "w") as file:

        json.dump(
            stats,
            file,
            indent=4
        )


def show_statistics():

    print("\n")
    print("=" * 40)
    print("NETWORK TRAFFIC STATISTICS")
    print("=" * 40)

    for key, value in stats.items():

        print(f"{key}: {value}")

    print("=" * 40)

    save_statistics()
