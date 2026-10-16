import os
import subprocess
import sys
from pathlib import Path

records = Path(os.environ.get("TRACKER_RECORDS", "records.json"))
notifications = Path(os.environ.get("TRACKER_NOTIFICATIONS", "notifications.log"))
records.write_text("[]\n")
with notifications.open("a") as log:
    log.write("Synthetic shared-target reset and notification\n")
raise SystemExit(
    subprocess.run(
        [sys.executable, "-m", "unittest", "discover", "-s", "tests"], check=False
    ).returncode
)
