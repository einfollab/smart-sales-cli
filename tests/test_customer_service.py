import unittest
import os
import json

from customer_service import (
    register, list_all, detail, search, update, delete, exists
)

CUSTOMER_FILE = 'data/customers.json'
REPORT_FILE = 'data/sales_reports.json'


class TestCustomerService(unittest.TestCase):

    def setUp(self):
        # 실제 데이터 파일을 백업하고 빈 배열로 초기화
        self._backup = None
        if os.path.exists(CUSTOMER_FILE):
            with open(CUSTOMER_FILE, 'r', encoding='utf-8') as f:
                self._backup = f.read()
        with open(CUSTOMER_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f)

    def tearDown(self):
        # 복원
        if self._backup is not None:
            with open(CUSTOMER_FILE, 'w', encoding='utf-8') as f:
                f.write(self._backup)

    # --- register ---
    def test_register_success(self):
        success, msg = register("테스트고객사", "홍길동", "hong@example.com")
        self.assertTrue(success)
        self.assertIn("C001", msg)
        customers = list_all()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0]['customer_id'], "C001")

    def test_register_auto_increment_id(self):
        register("A", "M1", "a@test.com")
        register("B", "M2", "b@test.com")
        customers = list_all()
        self.assertEqual(len(customers), 2)
        self.assertEqual(customers[0]['customer_id'], "C001")
        self.assertEqual(customers[1]['customer_id'], "C002")

    def test_register_empty_name_fails(self):
        success, msg = register("", "홍길동", "hong@example.com")
        self.assertFalse(success)

    def test_register_empty_manager_fails(self):
        success, msg = register("테스트", "", "hong@example.com")
        self.assertFalse(success)

    def test_register_invalid_email_fails(self):
        success, msg = register("테스트", "홍길동", "invalid")
        self.assertFalse(success)

    # --- list_all ---
    def test_list_all_empty(self):
        self.assertEqual(list_all(), [])

    def test_list_all_returns_all(self):
        register("A", "M1", "a@test.com")
        register("B", "M2", "b@test.com")
        customers = list_all()
        self.assertEqual(len(customers), 2)

    # --- detail ---
    def test_detail_existing(self):
        register("A", "M1", "a@test.com")
        c = detail("C001")
        self.assertIsNotNone(c)
        self.assertEqual(c['customer_name'], "A")

    def test_detail_nonexistent(self):
        self.assertIsNone(detail("C999"))

    # --- search ---
    def test_search_by_name(self):
        register("가나다", "홍길동", "hong@test.com")
        register("ABC", "김철수", "kim@test.com")
        results = search("가나")
        self.assertEqual(len(results), 1)

    def test_search_by_manager(self):
        register("가나다", "홍길동", "hong@test.com")
        results = search("홍길")
        self.assertEqual(len(results), 1)

    def test_search_empty_keyword_returns_all(self):
        register("A", "M1", "a@test.com")
        results = search("")
        self.assertEqual(len(results), 1)

    def test_search_no_match(self):
        register("A", "M1", "a@test.com")
        results = search("ZZZ")
        self.assertEqual(len(results), 0)

    # --- update ---
    def test_update_name(self):
        register("A", "M1", "a@test.com")
        success, msg = update("C001", customer_name="B")
        self.assertTrue(success)
        c = detail("C001")
        self.assertEqual(c['customer_name'], "B")

    def test_update_manager(self):
        register("A", "M1", "a@test.com")
        success, msg = update("C001", manager_name="M2")
        self.assertTrue(success)
        c = detail("C001")
        self.assertEqual(c['manager_name'], "M2")

    def test_update_email(self):
        register("A", "M1", "a@test.com")
        success, msg = update("C001", email="new@test.com")
        self.assertTrue(success)
        c = detail("C001")
        self.assertEqual(c['email'], "new@test.com")

    def test_update_nonexistent(self):
        success, msg = update("C999", customer_name="B")
        self.assertFalse(success)

    def test_update_invalid_email_fails(self):
        register("A", "M1", "a@test.com")
        success, msg = update("C001", email="bad")
        self.assertFalse(success)

    def test_update_customer_id_unchanged(self):
        register("A", "M1", "a@test.com")
        update("C001", customer_name="B")
        c = detail("C001")
        self.assertEqual(c['customer_id'], "C001")

    # --- delete ---
    def test_delete_existing(self):
        register("A", "M1", "a@test.com")
        success, msg = delete("C001")
        self.assertTrue(success)
        self.assertEqual(len(list_all()), 0)

    def test_delete_nonexistent(self):
        success, msg = delete("C999")
        self.assertFalse(success)

    def test_delete_partial(self):
        register("A", "M1", "a@test.com")
        register("B", "M2", "b@test.com")
        delete("C001")
        customers = list_all()
        self.assertEqual(len(customers), 1)
        self.assertEqual(customers[0]['customer_id'], "C002")

    # --- exists ---
    def test_exists_true(self):
        register("A", "M1", "a@test.com")
        self.assertTrue(exists("C001"))

    def test_exists_false(self):
        self.assertFalse(exists("C999"))


if __name__ == '__main__':
    unittest.main()