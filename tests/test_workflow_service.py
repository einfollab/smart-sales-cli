import unittest
import os
import json

from customer_service import register as register_customer
from report_service import register as register_report
from workflow_service import submit, approve, reject, withdraw

CUSTOMER_FILE = 'data/customers.json'
REPORT_FILE = 'data/sales_reports.json'


class TestWorkflowService(unittest.TestCase):

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
        register_report("C001", "2026-06-09", "제품 소개 미팅")

    def tearDown(self):
        if self._backup_c is not None:
            with open(CUSTOMER_FILE, 'w', encoding='utf-8') as f:
                f.write(self._backup_c)
        if self._backup_r is not None:
            with open(REPORT_FILE, 'w', encoding='utf-8') as f:
                f.write(self._backup_r)

    # --- submit: DRAFT → SUBMITTED ---
    def test_submit_from_draft_success(self):
        success, msg = submit("R001")
        self.assertTrue(success)
        self.assertIn("DRAFT → SUBMITTED", msg)

    def test_submit_nonexistent_fails(self):
        success, msg = submit("R999")
        self.assertFalse(success)

    def test_submit_twice_fails(self):
        submit("R001")
        success, msg = submit("R001")
        self.assertFalse(success)

    # --- approve: SUBMITTED → APPROVED ---
    def test_approve_from_submitted_success(self):
        submit("R001")
        success, msg = approve("R001")
        self.assertTrue(success)
        self.assertIn("SUBMITTED → APPROVED", msg)

    def test_approve_from_draft_fails(self):
        success, msg = approve("R001")
        self.assertFalse(success)

    def test_approve_from_approved_fails(self):
        submit("R001")
        approve("R001")
        success, msg = approve("R001")
        self.assertFalse(success)

    # --- reject: SUBMITTED → REJECTED ---
    def test_reject_from_submitted_success(self):
        submit("R001")
        success, msg = reject("R001")
        self.assertTrue(success)
        self.assertIn("SUBMITTED → REJECTED", msg)

    def test_reject_from_draft_fails(self):
        success, msg = reject("R001")
        self.assertFalse(success)

    # --- withdraw: SUBMITTED → DRAFT ---
    def test_withdraw_from_submitted_success(self):
        submit("R001")
        success, msg = withdraw("R001")
        self.assertTrue(success)
        self.assertIn("SUBMITTED → DRAFT", msg)

    def test_withdraw_from_draft_fails(self):
        success, msg = withdraw("R001")
        self.assertFalse(success)

    def test_withdraw_from_approved_fails(self):
        submit("R001")
        approve("R001")
        success, msg = withdraw("R001")
        self.assertFalse(success)

    def test_withdraw_from_rejected_fails(self):
        submit("R001")
        reject("R001")
        success, msg = withdraw("R001")
        self.assertFalse(success)

    # --- full workflow ---
    def test_full_workflow_submit_approve(self):
        success1, _ = submit("R001")
        self.assertTrue(success1)
        success2, _ = approve("R001")
        self.assertTrue(success2)

    def test_full_workflow_submit_reject(self):
        submit("R001")
        success, _ = reject("R001")
        self.assertTrue(success)

    def test_full_workflow_submit_withdraw_resubmit(self):
        submit("R001")
        withdraw("R001")
        success, _ = submit("R001")
        self.assertTrue(success)


if __name__ == '__main__':
    unittest.main()