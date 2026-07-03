import re
from datetime import datetime


def validate_required(value, name):
    """필수 입력값 검증. 빈 문자열이나 공백이면 오류 메시지 반환."""
    if not value or not value.strip():
        return f"{name}은(는) 필수 입력값입니다."
    return None


def validate_customer_id(cid):
    """고객 ID 형식 검증: C + 3자리 숫자 (C001~C999)."""
    error = validate_required(cid, "고객 ID")
    if error:
        return error
    if not re.match(r'^C\d{3}$', cid):
        return "고객 ID는 'C' 뒤에 3자리 숫자 형식이어야 합니다. (예: C001)"
    if cid == "C000":
        return "고객 ID는 C001부터 C999까지 사용 가능합니다."
    return None


def validate_email(email):
    """이메일 형식 검증."""
    error = validate_required(email, "이메일")
    if error:
        return error
    if '@' not in email or email.count('@') != 1:
        return "올바른 이메일 형식이 아닙니다."
    local, domain = email.split('@')
    if not local or not domain:
        return "올바른 이메일 형식이 아닙니다."
    if '.' not in domain:
        return "올바른 이메일 형식이 아닙니다."
    return None


def validate_date(date_str):
    """날짜 형식 검증: YYYY-MM-DD + 실제 존재하는 날짜."""
    error = validate_required(date_str, "날짜")
    if error:
        return error
    if not re.match(r'^\d{4}-\d{2}-\d{2}$', date_str):
        return "날짜는 YYYY-MM-DD 형식이어야 합니다. (예: 2026-06-09)"
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return None
    except ValueError:
        return "존재하지 않는 날짜입니다."