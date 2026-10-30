# Multi-Layer Network Traffic Analysis and Threat Detection Framework

A Python and Scapy project that monitors network packets, classifies protocols, maps traffic to OSI layers, detects selected DNS and port-scan-like events, saves alerts to CSV, and generates traffic-analysis graphs.

Developed in **Kali Linux** with an **Ubuntu Server virtual machine** as a lab endpoint. This guide is written for first-time users.

> **Authorised use only:** Run tests only on your own virtual machines or a network for which you have explicit permission. This is an academic prototype; an alert is not proof of compromise.

## Contents

1. [What You Need](#1-what-you-need)
2. [Lab Setup on macOS, Windows, or Linux](#2-lab-setup-on-macos-windows-or-linux)
3. [Project Files](#3-project-files)
4. [Install Packages in Kali](#4-install-packages-in-kali)
5. [Check the Kali–Ubuntu Connection](#5-check-the-kaliubuntu-connection)
6. [Start the Framework](#6-start-the-framework)
7. [Test the Detectors](#7-test-the-detectors)
8. [Review CSV and JSON Reports](#8-review-csv-and-json-reports)
9. [Generate Graphs](#9-generate-graphs)
10. [Analyse a Saved PCAP](#10-analyse-a-saved-pcap)
11. [Troubleshooting](#11-troubleshooting)
12. [License](#12-license)

## 1. What You Need

- A host computer running **macOS, Windows, or Linux**.
- A virtualisation application:
  - **macOS:** UTM (used during development) or another compatible VM application.
  - **Windows:** VirtualBox or VMware Workstation.
  - **Linux:** VirtualBox, VMware, or another compatible VM application.
- A **Kali Linux VM** to run the framework.
- An **Ubuntu Server VM** to act as the test endpoint.
- Internet access for package installation.
- Recommended starting resources: 2 virtual CPUs and 4 GB RAM for Kali, plus resources for Ubuntu. Actual requirements depend on the host and VM settings.
- Both VMs connected to the same **isolated or host-only virtual network**, where practical.

The project is run **inside Kali Linux**. The host OS runs the virtualisation software.

## 2. Lab Setup on macOS, Windows, or Linux

1. Install a virtualisation application for your host OS.
2. Create a Kali Linux VM and an Ubuntu Server VM.
3. Connect both VMs to the same virtual network. Prefer an isolated/host-only network instead of scanning devices on a home, university, workplace, or public network.
4. Start both VMs and log in.
5. On Ubuntu Server, run:

   ```bash
   ip -br address
   ```

   Record the Ubuntu VM's IP address.
6. In Kali, run:

   ```bash
   ip -br address
   ```

   Record the Kali VM's IP address and interface.

During development, Kali and Ubuntu used `192.168.64.3` and `192.168.64.4`, respectively. **Your addresses may differ; always use the addresses shown by your VMs.**

## 3. Project Files

The main project files include:

```text
network-monitor/
├── main.py
├── protocol_classifier.py
├── logger.py
├── statistics.py
├── layer_statistics.py
├── generate_graphs.py
├── layer_graph.py
├── threat_graph.py
├── capture_test.py
├── offline_analyzer.py
├── detectors/
│   ├── portscan_detector.py
│   └── dns_detector.py
├── logs/
│   └── alerts.csv
├── statistics.json
├── layer_statistics.json
├── test_capture.pcap
├── protocol_distribution.png
├── osi_layer_distribution.png
└── threat_detection.png
```

CSV, JSON, PCAP and PNG files may be created when you run the project. The detector files must be present because `main.py` imports them.

## 4. Install Packages in Kali

Open a terminal **inside the Kali VM**.

### Step 1 — Install system tools

```bash
sudo apt update
sudo apt install -y python3 python3-pip python3-venv git nmap tcpdump
```

### Step 2 — Download the repository

Copy your actual GitHub repository URL and run:

```bash
git clone <YOUR-GITHUB-REPOSITORY-URL>
cd <YOUR-REPOSITORY-FOLDER>
```

Replace the placeholders with your repository URL and folder name.

If the project is already located at `~/network-monitor`, run:

```bash
cd ~/network-monitor
```

### Step 3 — Install Python libraries

The framework uses **Scapy** for packet capture and **Matplotlib** for graphs. A virtual environment is the recommended option on Kali:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install scapy matplotlib
```

When the environment is active, run the framework with `sudo .venv/bin/python main.py` as shown below. This makes sure it uses the Python environment where Scapy and Matplotlib were installed.

If the repository provides a tested `requirements.txt`, you can install its dependencies instead with `python -m pip install -r requirements.txt`.

## 5. Check the Kali–Ubuntu Connection

Use your actual Ubuntu IP. The example below uses `192.168.64.4`.

From Kali:

```bash
ping -c 4 192.168.64.4
```

**Purpose:** sends four ICMP echo requests to Ubuntu. Replies indicate basic connectivity. If no replies arrive, check the VM network mode, IP addresses and firewall; some systems block ping even when other traffic works.

## 6. Start the Framework

From the project directory in Kali:

```bash
sudo .venv/bin/python main.py
```

You should see a startup message similar to:

```text
Starting Multi-Layer Network Traffic Analysis Framework...
Press CTRL + C to stop and generate reports.
```

### What happens while it runs?

1. Scapy captures packets visible on its selected/default interface.
2. `protocol_classifier.py` classifies supported protocols, including ARP, IP, ICMP, TCP, UDP and DNS, and maps them to conceptual OSI layers.
3. The detector modules check for selected port-scan-like activity and DNS queries.
4. `logger.py` records events in `logs/alerts.csv`.
5. When you stop the capture, the framework prints protocol and OSI-layer statistics and saves JSON reports.

Keep the terminal running while you generate test traffic. Stop capture with **Ctrl+C**.

> The current `main.py` calls Scapy's `sniff(...)` without specifying an interface. If your traffic is not visible, verify the VM network configuration and whether the default interface can see the traffic.

## 7. Test the Detectors

Keep the framework running in one Kali terminal. Generate traffic in another terminal or from Ubuntu.

### Test A — Ping the Ubuntu VM

```bash
ping -c 4 <UBUNTU-IP>
```

Replace `<UBUNTU-IP>` with your Ubuntu VM address. Visible packets may be classified as IP/ICMP and ICMP events may be logged.

### Test B — Generate DNS traffic

```bash
nslookup google.com
```

This requests DNS resolution. If the DNS packets are visible, the framework should classify DNS traffic and the DNS detector may report a query. Resolver configuration, caching and interface selection can affect results.

### Test C — Test port-scan detection with Nmap

Run this **only against your own Ubuntu lab VM**:

```bash
nmap -sT -p 1-100 <UBUNTU-IP>
```

This scans TCP ports 1–100 on the specified lab endpoint. The detector may trigger depending on its threshold, observation logic and whether the traffic is visible. A missing alert does not by itself prove that the framework is broken.

### Finish the test

Return to the framework terminal and press **Ctrl+C**. The program prints statistics and saves the JSON reports.

## 8. Review CSV and JSON Reports

Run these commands from the project directory after stopping capture.

### Alert log

```bash
cat logs/alerts.csv
```

The CSV columns include timestamp, alert type, source IP, destination IP and protocol. Events depend on the traffic observed. The logger creates the `logs/` directory and CSV header when the framework starts.

### Protocol and detection statistics

```bash
cat statistics.json
```

This contains counters for supported protocols and detector events, including `PortScanAlerts` and `DNSQueries`.

### OSI-layer statistics

```bash
cat layer_statistics.json
```

This contains counts for Data Link, Network, Transport and Application layers according to the project's mapping logic. Counts vary by run.

## 9. Generate Graphs

Run these commands **after stopping the framework**, so the JSON files have been written. Run them from the project directory.

### Protocol distribution graph

```bash
python3 generate_graphs.py
```

Reads `statistics.json` and saves `protocol_distribution.png`.

### OSI-layer distribution graph

```bash
python3 layer_graph.py
```

Reads `layer_statistics.json` and saves `osi_layer_distribution.png`.

### Threat-detection events graph

```bash
python3 threat_graph.py
```

Reads `statistics.json` and saves `threat_detection.png`.

Open the `.png` files using Kali's file manager or transfer them to the host computer. The charts show saved counts; they do not independently prove that an attack occurred.

## Viewing the Graphs 

Run this command after generating the graphs to view the graphs itself in the kali linux .

```bash
xdg-open osi_layer_distribution.png
```

## 10. Analyse a Saved PCAP

The helper `capture_test.py` captures 50 packets and saves them to `test_capture.pcap`. Run it only in your authorised lab:

```bash
sudo .venv/bin/python capture_test.py
```

It waits until 50 packets have been captured. Generate some lab traffic while it runs if needed.

Then run the offline classifier:

```bash
.venv/bin/python offline_analyzer.py
```

The analyzer reads `test_capture.pcap`, prints packet classifications, and reports the number of packets analysed. It is a basic offline classifier and does not run the full live detection/logging pipeline.

To inspect the PCAP with tcpdump:

```bash
tcpdump -nn -r test_capture.pcap
```

## 11. Troubleshooting

### Scapy or Matplotlib is missing

```bash
source .venv/bin/activate
python -m pip install scapy matplotlib
```

Run the framework using `sudo .venv/bin/python main.py`.

### `ModuleNotFoundError` for `detectors`

Make sure these files exist in the project:

```text
detectors/portscan_detector.py
detectors/dns_detector.py
```

### No packets or alerts appear

- Start the framework before generating test traffic.
- Check the VM IP addresses and network mode.
- Confirm that Scapy's default interface can see the traffic.
- Test only against your own Ubuntu VM.
- Alerts depend on the detector rules and thresholds.

### A graph reports that a JSON file is missing

Run `main.py`, generate some traffic, and stop it with Ctrl+C. Then run the graph command again from the project directory.

### Nmap is missing

```bash
sudo apt install -y nmap
```

## 12. License



```text
MIT License

Copyright (c) 2026 Shivam Gautam

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
