import json

layer_stats = {

    "Data Link Layer": 0,
    "Network Layer": 0,
    "Transport Layer": 0,
    "Application Layer": 0
}


def increment_layer(layer):

    if layer in layer_stats:
        layer_stats[layer] += 1


def save_layer_statistics():

    with open("layer_statistics.json", "w") as file:

        json.dump(
            layer_stats,
            file,
            indent=4
        )


def show_layer_statistics():

    total_packets = sum(layer_stats.values())

    print("\n")
    print("=" * 50)
    print("OSI LAYER ANALYSIS REPORT")
    print("=" * 50)

    for layer, count in layer_stats.items():

        percentage = 0

        if total_packets > 0:

            percentage = (
                count / total_packets
            ) * 100

        print(
            f"{layer}: "
            f"{count} packets "
            f"({percentage:.2f}%)"
        )

    print("=" * 50)

    save_layer_statistics()
