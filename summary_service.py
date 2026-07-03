from storage import load_data, save_data
from customer_service import detail as customer_detail

REPORT_FILE = 'data/sales_reports.json'


def summarize_by_customer(customer_id):
    """고객사별 활동 요약.
    반환: (성공여부, 데이터_또는_오류메시지)
    데이터: {
        'customer_id': ..., 'customer_name': ...,
        'total_reports': N, 'approved_reports': N,
        'reports': [...]
    }
    """
    customer = customer_detail(customer_id)
    if customer is None:
        return False, "존재하지 않는 고객사입니다."

    reports = load_data(REPORT_FILE)
    customer_reports = [r for r in reports if r['customer_id'] == customer_id]

    approved = [r for r in customer_reports if r['status'] == 'APPROVED']

    result = {
        'customer_id': customer['customer_id'],
        'customer_name': customer['customer_name'],
        'total_reports': len(customer_reports),
        'approved_reports': len(approved),
        'reports': customer_reports
    }
    return True, result