import unittest
import os
import json

from customer_service import register as register_customer
from report_service import register as register_report
from workflow_service import submit, approve
from summary_service import summarize_by_customer

CUSTOMER_FILE = 'data/customers.json'
REPORT_FILE = 'data/sales_reports.json'


class TestSummaryService(unittest.TestCase):

    def setUp(self):
        self._backup_c = None
        self._backup_r = None
        if os.path.exists(CUSTOMER_FILE):
            with open(CUSTOMER_FILE, 'r', encoding='utf-8') as f:
                self._backup_c = f.read()
        if os.path.exists(REPORT_FILE):
            with open(REPORT_FILE, 'r', encoding='utf-8') as f:
                self._backup_r = f.read()
        with open(CUSTOMER_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)
        with open(REPORT_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

        register_customer("테스트고객사", "홍길동", "hong@example.com")

    def tearDown(self):
        if self._backup_c is not None:
            with open(CUSTOMER_FILE, 'w', encoding='utf-8') as f:
                f.write(self._backup_c)
        if self._backup_r is not None:
            with open(REPORT_FILE, 'w', encoding='utf-8') as f:
                f.write(self._backup_r)

    def test_summarize_nonexistent_customer(self):
        success, data = summarize_by_customer("C999")
        self.assertFalse(success)

    def test_summarize_no_reports(self):
        success, data = summarize_by_customer("C001")
        self.assertTrue(success)
        self.assertEqual(data['total_reports'], 0)
        self.assertEqual(data['approved_reports'], 0)
        self.assertEqual(data['customer_name'], "테스트고객사")

    def test_summarize_with_draft_reports_only(self):
        register_report("C001", "2026-06-09", "미팅1")
        register_report("C001", "2026-06-10", "미팅2")
        success, data = summarize_by_customer("C001")
        self.assertTrue(success)
        self.assertEqual(data['total_reports'], 2)
        self.assertEqual(data['approved_reports'], 0)

    def test_summarize_with_approved_reports(self):
        register_report("C001", "2026-06-09", "미팅1")
        register_report("C001", "2026-06-10", "미팅2")
        submit("R001")
        approve("R001")
        success, data = summarize_by_customer("C001")
        self.assertTrue(success)
        self.assertEqual(data['total_reports'], 2)
        self.assertEqual(data['approved_reports'], 1)

    def test_summarize_reports_list_format(self):
        register_report("C001", "2026-06-09", "미팅")
        success, data = summarize_by_customer("C001")
        self.assertTrue(success)
        self.assertIsInstance(data['reports'], list)
        self.assertEqual(len(data['reports']), 1)
        self.assertIn('report_id', data['reports'][0])
        self.assertIn('status', data['reports'][0])


if __name__ == '__main__':
    unittest.main()