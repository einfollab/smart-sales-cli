import unittest
import os
import json

from customer_service import register as register_customer
from sales_report_service import (
    register, list_all, get_by_id, update
)

CUSTOMER_FILE = 'data/customers.json'
REPORT_FILE = 'data/sales_reports.json'


class TestSalesReportService(unittest.TestCase):

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
        """신규 영업일지 등록 성공"""
        success, msg = register("C001", "2026-06-09", "제품 소개 미팅")
        self.assertTrue(success)
        self.assertIn("R001", msg)

    def test_register_auto_increment_id(self):
        """영업일지 ID 자동 증가"""
        register("C001", "2026-06-09", "미팅1")
        register("C001", "2026-06-10", "미팅2")
        reports = list_all()
        self.assertEqual(len(reports), 2)
        self.assertEqual(reports[0]['report_id'], "R001")
        self.assertEqual(reports[1]['report_id'], "R002")

    def test_register_nonexistent_customer_fails(self):
        """존재하지 않는 고객사로 등록 실패"""
        success, msg = register("C999", "2026-06-09", "내용")
        self.assertFalse(success)
        self.assertIn("존재하지 않는", msg)

    def test_register_invalid_date_fails(self):
        """잘못된 날짜 형식 등록 실패"""
        success, msg = register("C001", "2026/06/09", "내용")
        self.assertFalse(success)

    def test_register_empty_content_fails(self):
        """빈 내용 등록 실패"""
        success, msg = register("C001", "2026-06-09", "")
        self.assertFalse(success)

    def test_register_initial_status_is_draft(self):
        """신규 영업일지는 DRAFT 상태"""
        register("C001", "2026-06-09", "미팅")
        r = get_by_id("R001")
        self.assertEqual(r['status'], "DRAFT")

    # --- list_all ---
    def test_list_all_empty(self):
        """빈 목록 조회"""
        self.assertEqual(len(list_all()), 0)

    def test_list_all_includes_customer_name(self):
        """목록에 고객사명 포함 확인"""
        register("C001", "2026-06-09", "미팅")
        reports = list_all()
        self.assertIn('customer_name', reports[0])
        self.assertEqual(reports[0]['customer_name'], "테스트고객사")

    # --- get_by_id ---
    def test_get_by_id_existing(self):
        """존재하는 영업일지 단건 조회"""
        register("C001", "2026-06-09", "미팅")
        r = get_by_id("R001")
        self.assertIsNotNone(r)
        self.assertEqual(r['content'], "미팅")

    def test_get_by_id_nonexistent(self):
        """존재하지 않는 영업일지 단건 조회"""
        self.assertIsNone(get_by_id("R999"))

    # --- update ---
    def test_update_content_success(self):
        """DRAFT 상태 영업일지 내용 수정 성공"""
        register("C001", "2026-06-09", "미팅")
        success, msg = update("R001", content="수정된 내용")
        self.assertTrue(success)
        r = get_by_id("R001")
        self.assertEqual(r['content'], "수정된 내용")

    def test_update_date_success(self):
        """DRAFT 상태 영업일지 날짜 수정 성공"""
        register("C001", "2026-06-09", "미팅")
        success, msg = update("R001", activity_date="2026-06-10")
        self.assertTrue(success)
        r = get_by_id("R001")
        self.assertEqual(r['activity_date'], "2026-06-10")

    def test_update_nonexistent_fails(self):
        """존재하지 않는 영업일지 수정 실패"""
        success, msg = update("R999", content="내용")
        self.assertFalse(success)

    def test_update_invalid_date_fails(self):
        """잘못된 날짜 형식 수정 실패"""
        register("C001", "2026-06-09", "미팅")
        success, msg = update("R001", activity_date="bad-date")
        self.assertFalse(success)

    def test_update_approved_report_fails(self):
        """APPROVED 상태 영업일지 수정 차단"""
        register("C001", "2026-06-09", "미팅")
        # 직접 JSON 파일을 수정하여 APPROVED 상태로 변경
        with open(REPORT_FILE, 'r', encoding='utf-8') as f:
            reports = json.load(f)
        for r in reports:
            if r['report_id'] == 'R001':
                r['status'] = 'APPROVED'
        with open(REPORT_FILE, 'w', encoding='utf-8') as f:
            json.dump(reports, f)

        success, msg = update("R001", content="수정 시도")
        self.assertFalse(success)
        self.assertIn("승인된", msg)

        # 데이터가 실제로 변경되지 않았는지 확인
        r = get_by_id("R001")
        self.assertEqual(r['content'], "미팅")


if __name__ == '__main__':
    unittest.main()