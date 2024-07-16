import unittest
from datetime import datetime
import pandas as pd
from src.utils import read_excel_data


class TestReadExcelData(unittest.TestCase):

    def setUp(self):
        # Create a sample Excel file (could use in-memory if preferred)
        self.file_path = 'test_data.xlsx'
        self.test_data = {
            'date': pd.date_range('2024-01-01', periods=10, freq='D'),
            'value': range(10)
        }
        self.df = pd.DataFrame(self.test_data)
        self.df.to_excel(self.file_path, index=False)

    def tearDown(self):
        import os
        os.remove(self.file_path)

    def test_basic_functionality(self):
        end_date = datetime.strptime('2024-01-15', '%Y-%m-%d')  # Преобразуем строку в datetime
        expected_result = self.df[self.df['date'] <= end_date]
        result = read_excel_data(self.file_path, end_date)
        pd.testing.assert_frame_equal(result, expected_result)

    def test_edge_case_start_of_month(self):
        end_date = datetime.strptime('2024-01-01', '%Y-%m-%d')  # Преобразуем строку в datetime
        expected_result = self.df[self.df['date'] <= end_date]
        result = read_excel_data(self.file_path, end_date)
        pd.testing.assert_frame_equal(result, expected_result)

    def test_edge_case_end_of_month(self):
        end_date = datetime.strptime('2024-01-31', '%Y-%m-%d')  # Преобразуем строку в datetime
        expected_result = self.df[self.df['date'] <= end_date]
        result = read_excel_data(self.file_path, end_date)
        pd.testing.assert_frame_equal(result, expected_result)

    def test_empty_dataframe(self):
        # Create an empty Excel file
        empty_file_path = 'empty.xlsx'
        pd.DataFrame(columns=['date', 'value']).to_excel(empty_file_path, index=False)
        result = read_excel_data(empty_file_path, datetime.strptime('2024-01-15', '%Y-%m-%d'))
        self.assertTrue(result.empty)
        import os
        os.remove(empty_file_path)

if __name__ == '__main__':
    unittest.main()