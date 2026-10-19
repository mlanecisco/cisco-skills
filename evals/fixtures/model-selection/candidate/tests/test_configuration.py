import unittest

from configuration import resolve_url


class ConfigurationTests(unittest.TestCase):
    def test_new_client(self):
        self.assertEqual(resolve_url({"service_url": "https://new.invalid"}), "https://new.invalid")

    def test_default(self):
        self.assertEqual(resolve_url({}), "https://default.invalid")
