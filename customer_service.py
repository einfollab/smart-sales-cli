from storage import load_data, save_data
from validator import (
    validate_required,
    validate_customer_id,
    validate_email
)

CUSTOMER_FILE = 'data/customers.json'
REPORT_FILE = 'data/sales_reports.json'


def _next_customer_id(customers):
    """기존 고객 ID 중 최대값 + 1 반환. 없으면 C001."""
    max_num = 0
    for c in customers:
        cid = c.get('customer_id', '')
        if cid.startswith('C') and cid[1:].isdigit():
            num = int(cid[1:])
            if num > max_num:
                max_num = num
    next_num = max_num + 1
    return f"C{next_num:03d}"


def register(customer_name, manager_name, email):
    """고객사 등록. 성공 시 (True, 메시지), 실패 시 (False, 오류메시지)."""
    # 입력 검증
    err = validate_required(customer_name, "고객사명")
    if err:
        return False, err
    err = validate_required(manager_name, "담당자명")
    if err:
        return False, err
    err = validate_email(email)
    if err:
        return False, err

    customers = load_data(CUSTOMER_FILE)
    cid = _next_customer_id(customers)

    customer = {
        "customer_id": cid,
        "customer_name": customer_name.strip(),
        "manager_name": manager_name.strip(),
        "email": email.strip()
    }
    customers.append(customer)
    save_data(CUSTOMER_FILE, customers)
    return True, f"고객사 등록 완료: {cid}"


def list_all():
    """전체 고객사 목록 반환."""
    return load_data(CUSTOMER_FILE)


def detail(customer_id):
    """고객사 상세 조회. 존재하지 않으면 None 반환."""
    customers = load_data(CUSTOMER_FILE)
    for c in customers:
        if c['customer_id'] == customer_id:
            return c
    return None


def search(keyword):
    """고객사명 또는 담당자명으로 검색. 빈 키워드면 전체 목록 반환."""
    if not keyword or not keyword.strip():
        return load_data(CUSTOMER_FILE)
    kw = keyword.strip().lower()
    customers = load_data(CUSTOMER_FILE)
    results = []
    for c in customers:
        if kw in c['customer_name'].lower() or kw in c['manager_name'].lower():
            results.append(c)
    return results


def update(customer_id, customer_name=None, manager_name=None, email=None):
    """고객사 정보 수정. customer_id는 변경 불가.
    None이 아닌 값만 업데이트."""
    customers = load_data(CUSTOMER_FILE)
    target = None
    for c in customers:
        if c['customer_id'] == customer_id:
            target = c
            break
    if target is None:
        return False, "존재하지 않는 고객사입니다."

    if customer_name is not None:
        err = validate_required(customer_name, "고객사명")
        if err:
            return False, err
        target['customer_name'] = customer_name.strip()

    if manager_name is not None:
        err = validate_required(manager_name, "담당자명")
        if err:
            return False, err
        target['manager_name'] = manager_name.strip()

    if email is not None:
        err = validate_email(email)
        if err:
            return False, err
        target['email'] = email.strip()

    save_data(CUSTOMER_FILE, customers)
    return True, f"고객사 정보 수정 완료: {customer_id}"


def delete(customer_id):
    """고객사 삭제. 영업일지는 유지."""
    customers = load_data(CUSTOMER_FILE)
    for i, c in enumerate(customers):
        if c['customer_id'] == customer_id:
            del customers[i]
            save_data(CUSTOMER_FILE, customers)
            return True, f"고객사 삭제 완료: {customer_id}"
    return False, "존재하지 않는 고객사입니다."


def exists(customer_id):
    """고객사 존재 여부 확인."""
    customers = load_data(CUSTOMER_FILE)
    for c in customers:
        if c['customer_id'] == customer_id:
            return True
    return False