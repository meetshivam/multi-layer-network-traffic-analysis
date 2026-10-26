import csv
import os
from datetime import datetime

LOG_FILE = "logs/alerts.csv"

def initialize_logger():

    if not os.path.exists("logs"):
        os.makedirs("logs")

    if not os.path.exists(LOG_FILE):

        with open(LOG_FILE, "w", newline="") as file:

            writer = csv.writer(file)

            writer.writerow([
                "Timestamp",
                "Alert Type",
                "Source IP",
                "Destination IP",
                "Protocol"
            ])

def log_alert(alert_type, src_ip, dst_ip, protocol):

    with open(LOG_FILE, "a", newline="") as file:

        writer = csv.writer(file)

        writer.writerow([
            datetime.now(),
            alert_type,
            src_ip,
            dst_ip,
            protocol
        ])
