from storage import load_data, save_data
from report_service import get_by_id

REPORT_FILE = 'data/sales_reports.json'

# 상태 전이 규칙: (현재 상태, action) -> 변경 상태
TRANSITIONS = {
    ('DRAFT', 'submit'): 'SUBMITTED',
    ('SUBMITTED', 'approve'): 'APPROVED',
    ('SUBMITTED', 'reject'): 'REJECTED',
    ('SUBMITTED', 'withdraw'): 'DRAFT',
}


def _change_status(report_id, action):
    """내부 상태 전이 처리."""
    reports = load_data(REPORT_FILE)
    target = None
    for r in reports:
        if r['report_id'] == report_id:
            target = r
            break
    if target is None:
        return False, "존재하지 않는 영업일지입니다."

    current = target['status']
    key = (current, action)
    if key not in TRANSITIONS:
        return False, f"'{current}' 상태에서 '{action}' 작업을 수행할 수 없습니다."

    new_status = TRANSITIONS[key]
    target['status'] = new_status
    save_data(REPORT_FILE, reports)
    return True, f"영업일지 {report_id} 상태 변경: {current} → {new_status}"


def submit(report_id):
    """상신: DRAFT → SUBMITTED"""
    return _change_status(report_id, 'submit')


def approve(report_id):
    """승인: SUBMITTED → APPROVED"""
    return _change_status(report_id, 'approve')


def reject(report_id):
    """반려: SUBMITTED → REJECTED"""
    return _change_status(report_id, 'reject')


def withdraw(report_id):
    """회수: SUBMITTED → DRAFT"""
    return _change_status(report_id, 'withdraw')