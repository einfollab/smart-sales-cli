import sys
import io

from customer_service import list_all


def export_to_csv():
    """고객사 목록을 CSV 형식으로 콘솔에 출력."""
    customers = list_all()
    if not customers:
        print("등록된 고객사가 없습니다.")
        return

    output = io.StringIO()
    # 헤더
    output.write("customer_id,customer_name,manager_name,email\n")
    # 데이터 행
    for c in customers:
        name = c['customer_name'].replace('"', '""')
        manager = c['manager_name'].replace('"', '""')
        email = c['email'].replace('"', '""')
        output.write(f"{c['customer_id']},\"{name}\",\"{manager}\",\"{email}\"\n")

    print(output.getvalue())