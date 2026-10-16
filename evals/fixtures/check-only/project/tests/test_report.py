import unittest

from report import total


class ReportTests(unittest.TestCase):
    def test_values(self):
        self.assertEqual(total([10, 20, 0]), 30)

    def test_empty(self):
        self.assertEqual(total([]), 0)


if __name__ == "__main__":
    unittest.main()
