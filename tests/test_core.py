import os
import tempfile
import unittest

from llm_cost_guard import Tracker, BudgetExceeded, price_of, lookup


class PricingTests(unittest.TestCase):
    def test_prefix_match(self):
        self.assertEqual(lookup("gpt-4o-2024-08-06"), (2.50, 10.00))
        self.assertEqual(lookup("gpt-4o-mini-2024-07-18"), (0.15, 0.60))

    def test_cost(self):
        self.assertAlmostEqual(price_of("gpt-4o-mini", 1_000_000, 500_000), 0.45)


class TrackerTests(unittest.TestCase):
    def setUp(self):
        fd, self.path = tempfile.mkstemp(suffix=".db")
        os.close(fd)
        os.unlink(self.path)
        self.t = Tracker(self.path)

    def tearDown(self):
        self.t.close()
        os.unlink(self.path)

    def test_log_and_report(self):
        self.t.log("gpt-4o-mini", 1_000_000, 0, tag="a")
        self.t.log("deepseek-chat", 0, 1_000_000, tag="b")
        rows = self.t.report(by="model")
        self.assertEqual(len(rows), 2)
        self.assertAlmostEqual(rows[0]["cost_usd"], 1.10)  # deepseek output 1M

    def test_budget(self):
        self.t.log("gpt-4o", 1_000_000, 0)  # $2.50
        self.t.set_budget("monthly", 1.0)
        with self.assertRaises(BudgetExceeded):
            self.t.check_budget()
        self.t.set_budget("monthly", 100.0)
        self.t.check_budget()  # no raise


if __name__ == "__main__":
    unittest.main()
