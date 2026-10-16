import json
import os
import sys
from pathlib import Path


def save(name, amount):
    value = int(amount)
    records_path = Path(os.environ.get("TRACKER_RECORDS", "records.json"))
    notifications = Path(os.environ.get("TRACKER_NOTIFICATIONS", "notifications.log"))
    records = json.loads(records_path.read_text())
    records.append({"name": name, "amount": value})
    records_path.write_text(json.dumps(records) + "\n")
    with notifications.open("a") as log:
        log.write(f"Saved {name}\n")


if __name__ == "__main__":
    save(sys.argv[1], sys.argv[2])
