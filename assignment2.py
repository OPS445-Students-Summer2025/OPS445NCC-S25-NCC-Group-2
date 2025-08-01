#!/usr/bin/env python3

import os
import json
import csv
from datetime import datetime

def log_operation(op_type, source, destination):
    if not os.path.exists("logs"):
        os.mkdir("logs")

    log_entry = {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "operation": op_type,
        "source": source,
        "destination": destination
    }

    json_file = "logs/log.json"
    if os.path.exists(json_file):
        with open(json_file, "r") as jf:
            try:
                data = json.load(jf)
            except:
                data = []
    else:
        data = []

    data.append(log_entry)

    with open(json_file, "w") as jf:
        json.dump(data, jf, indent=2)

    print("JSON log saved!")

    csv_file = "logs/log.csv"
    write_header = not os.path.exists(csv_file)

    with open(csv_file, "a", newline='') as cf:
        writer = csv.writer(cf)
        if write_header:
            writer.writerow(["time", "operation", "source", "destination"])
        writer.writerow([
            log_entry["time"],
            log_entry["operation"],
            log_entry["source"],
            log_entry["destination"]
        ])
