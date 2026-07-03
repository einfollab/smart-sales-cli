import unittest
import os
import json

from customer_service import register as register_customer
from sales_report_service import register as register_report
from approval_service import submit, approve, reject, withdraw

CUSTOMER_FILE = 'data/customers.json'
REPORT_FILE = 'data/sales_reports.json'


class TestApprovalService(unittest.TestCase):

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

        # 테스트용 고객사 및 영업일지 등록
        register_customer("테스트고객사", "홍길동", "hong@example.com")
        register_report("C001", "2026-06-09", "미팅")

    def tearDown(self):
        if self._backup_c is not None:
            with open(CUSTOMER_FILE, 'w', encoding='utf-8') as f:
                f.write(self._backup_c)
        if self._backup_r is not None:
            with open(REPORT_FILE, 'w', encoding='utf-8') as f:
                f.write(self._backup_r)

    def _get_report_status(self, report_id):
        """JSON 파일에서 직접 영업일지 상태 조회"""
        with open(REPORT_FILE, 'r', encoding='utf-8') as f:
            reports = json.load(f)
        for r in reports:
            if r['report_id'] == report_id:
                return r['status']
        return None

    # --- submit ---
    def test_submit_from_draft_success(self):
        """DRAFT → SUBMITTED 성공"""
        success, msg = submit("R001")
        self.assertTrue(success)
        self.assertIn("DRAFT → SUBMITTED", msg)
        self.assertEqual(self._get_report_status("R001"), "SUBMITTED")

    def test_submit_nonexistent_fails(self):
        """존재하지 않는 영업일지 상신 실패"""
        success, msg = submit("R999")
        self.assertFalse(success)
        self.assertIn("존재하지 않는", msg)

    def test_submit_twice_fails(self):
        """이미 SUBMITTED 상태에서 재상신 실패"""
        submit("R001")
        success, msg = submit("R001")
        self.assertFalse(success)
        self.assertIn("수행할 수 없습니다", msg)

    # --- approve ---
    def test_approve_from_submitted_success(self):
        """SUBMITTED → APPROVED 성공"""
        submit("R001")
        success, msg = approve("R001")
        self.assertTrue(success)
        self.assertIn("SUBMITTED → APPROVED", msg)
        self.assertEqual(self._get_report_status("R001"), "APPROVED")

    def test_approve_from_draft_fails(self):
        """DRAFT 상태에서 승인 실패"""
        success, msg = approve("R001")
        self.assertFalse(success)
        self.assertIn("수행할 수 없습니다", msg)

    def test_approve_from_approved_fails(self):
        """이미 APPROVED 상태에서 재승인 실패"""
        submit("R001")
        approve("R001")
        success, msg = approve("R001")
        self.assertFalse(success)
        self.assertIn("수행할 수 없습니다", msg)

    # --- reject ---
    def test_reject_from_submitted_success(self):
        """SUBMITTED → REJECTED 성공"""
        submit("R001")
        success, msg = reject("R001")
        self.assertTrue(success)
        self.assertIn("SUBMITTED → REJECTED", msg)
        self.assertEqual(self._get_report_status("R001"), "REJECTED")

    def test_reject_from_draft_fails(self):
        """DRAFT 상태에서 반려 실패"""
        success, msg = reject("R001")
        self.assertFalse(success)
        self.assertIn("수행할 수 없습니다", msg)

    # --- withdraw ---
    def test_withdraw_from_submitted_success(self):
        """SUBMITTED → DRAFT 성공"""
        submit("R001")
        success, msg = withdraw("R001")
        self.assertTrue(success)
        self.assertIn("SUBMITTED → DRAFT", msg)
        self.assertEqual(self._get_report_status("R001"), "DRAFT")

    def test_withdraw_from_draft_fails(self):
        """DRAFT 상태에서 회수 실패"""
        success, msg = withdraw("R001")
        self.assertFalse(success)
        self.assertIn("수행할 수 없습니다", msg)

    def test_withdraw_from_approved_fails(self):
        """APPROVED 상태에서 회수 실패"""
        submit("R001")
        approve("R001")
        success, msg = withdraw("R001")
        self.assertFalse(success)
        self.assertIn("수행할 수 없습니다", msg)

    def test_withdraw_from_rejected_fails(self):
        """REJECTED 상태에서 회수 실패"""
        submit("R001")
        reject("R001")
        success, msg = withdraw("R001")
        self.assertFalse(success)
        self.assertIn("수행할 수 없습니다", msg)

    # --- full workflow ---
    def test_full_workflow_submit_approve(self):
        """전체 워크플로우: DRAFT → SUBMITTED → APPROVED"""
        self.assertEqual(self._get_report_status("R001"), "DRAFT")
        submit("R001")
        self.assertEqual(self._get_report_status("R001"), "SUBMITTED")
        approve("R001")
        self.assertEqual(self._get_report_status("R001"), "APPROVED")

    def test_full_workflow_submit_reject(self):
        """전체 워크플로우: DRAFT → SUBMITTED → REJECTED"""
        self.assertEqual(self._get_report_status("R001"), "DRAFT")
        submit("R001")
        self.assertEqual(self._get_report_status("R001"), "SUBMITTED")
        reject("R001")
        self.assertEqual(self._get_report_status("R001"), "REJECTED")

    def test_full_workflow_submit_withdraw_resubmit(self):
        """전체 워크플로우: DRAFT → SUBMITTED → DRAFT → SUBMITTED"""
        self.assertEqual(self._get_report_status("R001"), "DRAFT")
        submit("R001")
        self.assertEqual(self._get_report_status("R001"), "SUBMITTED")
        withdraw("R001")
        self.assertEqual(self._get_report_status("R001"), "DRAFT")
        submit("R001")
        self.assertEqual(self._get_report_status("R001"), "SUBMITTED")


if __name__ == '__main__':
    unittest.main()