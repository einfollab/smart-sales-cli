from storage import load_data, save_data
from validator import validate_required, validate_date
from customer_service import exists

REPORT_FILE = 'data/sales_reports.json'


def _next_report_id(reports):
    """기존 영업일지 ID 중 최대값 + 1 반환. 없으면 R001."""
    max_num = 0
    for r in reports:
        rid = r.get('report_id', '')
        if rid.startswith('R') and rid[1:].isdigit():
            num = int(rid[1:])
            if num > max_num:
                max_num = num
    next_num = max_num + 1
    return f"R{next_num:03d}"


def register(customer_id, activity_date, content):
    """영업일지 등록. 성공 시 (True, 메시지), 실패 시 (False, 오류메시지)."""
    err = validate_required(customer_id, "고객 ID")
    if err:
        return False, err
    err = validate_date(activity_date)
    if err:
        return False, err
    err = validate_required(content, "영업 활동 내용")
    if err:
        return False, err

    if not exists(customer_id):
        return False, "존재하지 않는 고객사입니다."

    reports = load_data(REPORT_FILE)
    rid = _next_report_id(reports)

    report = {
        "report_id": rid,
        "customer_id": customer_id.strip(),
        "activity_date": activity_date.strip(),
        "content": content.strip(),
        "status": "DRAFT"
    }
    reports.append(report)
    save_data(REPORT_FILE, reports)
    return True, f"영업일지 등록 완료: {rid}"


def list_all():
    """전체 영업일지 목록 반환. 고객사명을 포함하여 반환."""
    from customer_service import detail as customer_detail
    reports = load_data(REPORT_FILE)
    result = []
    for r in reports:
        entry = dict(r)
        c = customer_detail(r['customer_id'])
        entry['customer_name'] = c['customer_name'] if c else '알 수 없음'
        result.append(entry)
    return result


def get_by_id(report_id):
    """영업일지 단건 조회. 없으면 None 반환."""
    reports = load_data(REPORT_FILE)
    for r in reports:
        if r['report_id'] == report_id:
            return r
    return None


def update(report_id, content=None, activity_date=None):
    """영업일지 수정. 모든 상태에서 수정 가능.
    None이 아닌 값만 업데이트."""
    reports = load_data(REPORT_FILE)
    target = None
    for r in reports:
        if r['report_id'] == report_id:
            target = r
            break
    if target is None:
        return False, "존재하지 않는 영업일지입니다."

    if content is not None:
        err = validate_required(content, "영업 활동 내용")
        if err:
            return False, err
        target['content'] = content.strip()

    if activity_date is not None:
        err = validate_date(activity_date)
        if err:
            return False, err
        target['activity_date'] = activity_date.strip()

    save_data(REPORT_FILE, reports)
    return True, f"영업일지 수정 완료: {report_id}"


def delete(report_id):
    """영업일지 단독 삭제."""
    reports = load_data(REPORT_FILE)
    for i, r in enumerate(reports):
        if r['report_id'] == report_id:
            del reports[i]
            save_data(REPORT_FILE, reports)
            return True, f"영업일지 삭제 완료: {report_id}"
    return False, "존재하지 않는 영업일지입니다."