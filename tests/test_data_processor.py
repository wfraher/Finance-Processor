import unittest
import pandas as pd
from finance_processor import FinanceDataProcessor

class TestFinanceDataProcessor(unittest.TestCase):

    def setUp(self):
        # Path to original data
        self.raw_data_path = "tests/test_data/finance-charts-apple.csv"

        # Load data from values to compare to
        self.original_with_weekdays = pd.read_csv("tests/test_data/original_with_weekdays.csv", parse_dates=["Date"]).set_index("Date")
        self.above_average_volume = pd.read_csv("tests/test_data/above_average_volume.csv", parse_dates=["Date"]).set_index("Date")
        self.original_week_level = pd.read_csv("tests/test_data/original_week_level.csv", parse_dates=["Date"]).set_index("Date")
        self.higher_volume_week_level = pd.read_csv("tests/test_data/higher_volume_week_level.csv", parse_dates=["Date"]).set_index("Date")
        
        # Initialize the processor
        self.processor = FinanceDataProcessor("AAPL", self.raw_data_path)
        self.processor._add_day_of_week()

    def test_get_max(self):
        self.assertIsInstance(self.processor.get_max(), float)
        self.assertAlmostEqual(self.processor.get_max(), 136.270004)

    def test_get_min(self):
        self.assertIsInstance(self.processor.get_min(), float)
        self.assertAlmostEqual(self.processor.get_min(), 89.470001)

    def test_get_average(self):
        self.assertIsInstance(self.processor.get_average(), float)
        self.assertAlmostEqual(self.processor.get_average(), 112.95833971146244)

    def test_get_average_volume(self):
        self.assertIsInstance(self.processor.get_average_volume(), float)
        self.assertAlmostEqual(self.processor.get_average_volume(), 43178420.9486166)

    def test_remove_low_volume(self):
        result_df = self.processor.remove_low_volume_and_save("tests/outputs/above_average_volume_output.csv").set_index("Date")
        pd.testing.assert_frame_equal(result_df, self.above_average_volume)

    def test_generate_week_level(self):
        week_level_df = self.processor.generate_week_level(self.processor.raw_data, "tests/outputs/original_week_level_output.csv")
        week_level_df.index.freq = "W"
        self.original_week_level.index.freq = "W"
        pd.testing.assert_frame_equal(week_level_df, self.original_week_level)


    def test_validate(self):
        try:
            self.processor.validate()
        except AssertionError:
            self.fail("validate() raised AssertionError unexpectedly!")

if __name__ == '__main__':
    unittest.main()
