import unittest
import os
import json

from customer_service import register as register_customer
from report_service import (
    register, list_all, get_by_id, update, delete
)

CUSTOMER_FILE = 'data/customers.json'
REPORT_FILE = 'data/sales_reports.json'


class TestReportService(unittest.TestCase):

    def setUp(self):
        # 백업 후 초기화
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

        # 테스트용 고객사 등록
        register_customer("테스트고객사", "홍길동", "hong@example.com")

    def tearDown(self):
        if self._backup_c is not None:
            with open(CUSTOMER_FILE, 'w', encoding='utf-8') as f:
                f.write(self._backup_c)
        if self._backup_r is not None:
            with open(REPORT_FILE, 'w', encoding='utf-8') as f:
                f.write(self._backup_r)

    # --- register ---
    def test_register_success(self):
        success, msg = register("C001", "2026-06-09", "제품 소개 미팅")
        self.assertTrue(success)
        self.assertIn("R001", msg)

    def test_register_auto_increment_id(self):
        register("C001", "2026-06-09", "미팅1")
        register("C001", "2026-06-10", "미팅2")
        reports = list_all()
        self.assertEqual(len(reports), 2)
        self.assertEqual(reports[0]['report_id'], "R001")
        self.assertEqual(reports[1]['report_id'], "R002")

    def test_register_nonexistent_customer_fails(self):
        success, msg = register("C999", "2026-06-09", "내용")
        self.assertFalse(success)
        self.assertIn("존재하지 않는", msg)

    def test_register_invalid_date_fails(self):
        success, msg = register("C001", "2026/06/09", "내용")
        self.assertFalse(success)

    def test_register_empty_content_fails(self):
        success, msg = register("C001", "2026-06-09", "")
        self.assertFalse(success)

    # --- list_all ---
    def test_list_all_empty(self):
        self.assertEqual(len(list_all()), 0)

    def test_list_all_includes_customer_name(self):
        register("C001", "2026-06-09", "미팅")
        reports = list_all()
        self.assertIn('customer_name', reports[0])
        self.assertEqual(reports[0]['customer_name'], "테스트고객사")

    # --- get_by_id ---
    def test_get_by_id_existing(self):
        register("C001", "2026-06-09", "미팅")
        r = get_by_id("R001")
        self.assertIsNotNone(r)
        self.assertEqual(r['content'], "미팅")

    def test_get_by_id_nonexistent(self):
        self.assertIsNone(get_by_id("R999"))

    # --- update ---
    def test_update_content(self):
        register("C001", "2026-06-09", "미팅")
        success, msg = update("R001", content="수정된 내용")
        self.assertTrue(success)
        r = get_by_id("R001")
        self.assertEqual(r['content'], "수정된 내용")

    def test_update_date(self):
        register("C001", "2026-06-09", "미팅")
        success, msg = update("R001", activity_date="2026-06-10")
        self.assertTrue(success)
        r = get_by_id("R001")
        self.assertEqual(r['activity_date'], "2026-06-10")

    def test_update_nonexistent(self):
        success, msg = update("R999", content="내용")
        self.assertFalse(success)

    def test_update_invalid_date_fails(self):
        register("C001", "2026-06-09", "미팅")
        success, msg = update("R001", activity_date="bad-date")
        self.assertFalse(success)

    # --- delete ---
    def test_delete_existing(self):
        register("C001", "2026-06-09", "미팅")
        success, msg = delete("R001")
        self.assertTrue(success)
        self.assertEqual(len(list_all()), 0)

    def test_delete_nonexistent(self):
        success, msg = delete("R999")
        self.assertFalse(success)

    def test_delete_partial(self):
        register("C001", "2026-06-09", "미팅1")
        register("C001", "2026-06-10", "미팅2")
        delete("R001")
        reports = list_all()
        self.assertEqual(len(reports), 1)
        self.assertEqual(reports[0]['report_id'], "R002")


if __name__ == '__main__':
    unittest.main()