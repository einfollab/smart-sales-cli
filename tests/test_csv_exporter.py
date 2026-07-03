import unittest
import os
import json
import sys
import io

from customer_service import register as register_customer
from csv_exporter import export_to_csv

CUSTOMER_FILE = 'data/customers.json'


class TestCsvExporter(unittest.TestCase):

    def setUp(self):
        self._backup_c = None
        if os.path.exists(CUSTOMER_FILE):
            with open(CUSTOMER_FILE, 'r', encoding='utf-8') as f:
                self._backup_c = f.read()
        with open(CUSTOMER_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

    def tearDown(self):
        if self._backup_c is not None:
            with open(CUSTOMER_FILE, 'w', encoding='utf-8') as f:
                f.write(self._backup_c)

    def test_export_empty_returns_message(self):
        captured = io.StringIO()
        sys.stdout = captured
        export_to_csv()
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        self.assertIn("등록된 고객사가 없습니다", output)

    def test_export_contains_header(self):
        register_customer("테스트", "홍길동", "hong@test.com")
        captured = io.StringIO()
        sys.stdout = captured
        export_to_csv()
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        self.assertIn("customer_id,customer_name,manager_name,email", output)

    def test_export_contains_data(self):
        register_customer("테스트", "홍길동", "hong@test.com")
        captured = io.StringIO()
        sys.stdout = captured
        export_to_csv()
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        self.assertIn("C001", output)
        self.assertIn("테스트", output)
        self.assertIn("홍길동", output)
        self.assertIn("hong@test.com", output)

    def test_export_multiple_customers(self):
        register_customer("A", "M1", "a@test.com")
        register_customer("B", "M2", "b@test.com")
        captured = io.StringIO()
        sys.stdout = captured
        export_to_csv()
        sys.stdout = sys.__stdout__
        output = captured.getvalue()
        self.assertEqual(output.count("customer_id"), 1)  # 헤더 행에만
        self.assertEqual(output.count("C001"), 1)
        self.assertEqual(output.count("C002"), 1)

    def test_export_csv_format(self):
        register_customer("테스트", "홍길동", "hong@test.com")
        captured = io.StringIO()
        sys.stdout = captured
        export_to_csv()
        sys.stdout = sys.__stdout__
        lines = [l.strip() for l in captured.getvalue().strip().split('\n') if l.strip()]
        self.assertEqual(len(lines), 2)  # 헤더 + 데이터 1행
        self.assertTrue(lines[0].startswith("customer_id"))
        self.assertTrue(lines[1].startswith("C001"))


if __name__ == '__main__':
    unittest.main()