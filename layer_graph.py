import json
import matplotlib.pyplot as plt

with open("layer_statistics.json", "r") as file:
    layers = json.load(file)

layer_names = list(layers.keys())
layer_counts = list(layers.values())

plt.figure(figsize=(8, 5))

plt.bar(
    layer_names,
    layer_counts
)

plt.title(
    "OSI Layer Traffic Distribution"
)

plt.xlabel(
    "OSI Layers"
)

plt.ylabel(
    "Packet Count"
)

plt.tight_layout()

plt.savefig(
    "osi_layer_distribution.png"
)

print(
    "OSI Layer graph generated successfully."
)
