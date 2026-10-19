import unittest

from configuration import resolve_url


class ConfigurationTests(unittest.TestCase):
    def test_existing_client(self):
        self.assertEqual(resolve_url({"endpoint": "https://legacy.invalid"}), "https://legacy.invalid")

    def test_default(self):
        self.assertEqual(resolve_url({}), "https://default.invalid")
