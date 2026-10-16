import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from save import save


class SaveTests(unittest.TestCase):
    def test_whole_amount_is_saved(self):
        with tempfile.TemporaryDirectory() as location:
            root = Path(location)
            records = root / "records.json"
            records.write_text("[]\n")
            with patch.dict(os.environ, {
                "TRACKER_RECORDS": str(records),
                "TRACKER_NOTIFICATIONS": str(root / "notifications.log"),
            }):
                save("Workshop", "12")
            self.assertEqual(json.loads(records.read_text()), [{"name": "Workshop", "amount": 12}])
