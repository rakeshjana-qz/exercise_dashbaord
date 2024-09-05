# tests/test_csv_processor.py
import unittest
import os
import tempfile
import sys

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from csv_processor import convert_csv

class TestCSVProcessor(unittest.TestCase):
    def setUp(self):
        # Create a temporary directory to store test files
        self.test_dir = tempfile.TemporaryDirectory()

    def tearDown(self):
        # Cleanup the temporary directory
        self.test_dir.cleanup()

    def test_csv_conversion(self):
        # Paths for the input, output, and log CSV files
        input_csv = os.path.join(self.test_dir.name, "input.csv")
        output_csv = os.path.join(self.test_dir.name, "output.csv")
        log_csv = os.path.join(self.test_dir.name, "log.csv")

        # Write a sample CSV to the input path
        with open(input_csv, mode='w', newline='', encoding='utf-8') as file:
            file.write("ex_limit,questionified,specific_ids\n")
            file.write("5,true,123\n")

        # Run the conversion
        convert_csv(input_csv, output_csv, log_csv)

        # Assert that the output and log files were created
        self.assertTrue(os.path.exists(output_csv))
        self.assertTrue(os.path.exists(log_csv))

        # Check the contents of the output CSV
        with open(output_csv, mode='r', newline='', encoding='utf-8') as file:
            content = file.read()
            self.assertIn("generated_encoded_query_string", content)
            self.assertIn("5", content)

    def test_empty_csv(self):
        input_csv = os.path.join(self.test_dir.name, "empty_input.csv")
        output_csv = os.path.join(self.test_dir.name, "empty_output.csv")
        log_csv = os.path.join(self.test_dir.name, "empty_log.csv")

        with open(input_csv, mode='w', newline='', encoding='utf-8') as file:
            file.write("")

        # Run the conversion
        with self.assertRaises(ValueError):
            convert_csv(input_csv, output_csv, log_csv)

if __name__ == "__main__":
    unittest.main()