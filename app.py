def print_header(title):
    """헤더 출력"""
    print(f"\n{'=' * 50}")
    print(f"  {title}")
    print(f"{'=' * 50}")


def print_menu():
    """메인 메뉴 출력"""
    print("\n[ 스마트 세일즈 CLI ]")
    print("1. 고객사 등록")
    print("2. 고객사 목록")
    print("3. 고객사 상세 조회")
    print("4. 고객사 검색")
    print("5. 고객사 수정")
    print("6. 고객사 삭제")
    print("7. 영업일지 등록")
    print("8. 영업일지 목록")
    print("9. 영업일지 수정")
    print("10. 영업일지 삭제")
    print("11. 영업일지 상신")
    print("12. 영업일지 승인")
    print("13. 영업일지 반려")
    print("14. 영업일지 회수")
    print("15. 고객사별 활동 요약")
    print("16. 고객사 목록 CSV 내보내기")
    print("0. 종료")
    return input("\n메뉴를 선택하세요: ").strip()


def run():
    while True:
        choice = print_menu()

        if choice == '0':
            print("프로그램을 종료합니다.")
            break

        elif choice == '1':
            print_header("고객사 등록")
            name = input("고객사명: ").strip()
            manager = input("담당자명: ").strip()
            email = input("이메일: ").strip()
            from customer_service import register
            success, msg = register(name, manager, email)
            print(f"→ {msg}")

        elif choice == '2':
            print_header("고객사 목록")
            from customer_service import list_all
            customers = list_all()
            if not customers:
                print("등록된 고객사가 없습니다.")
            else:
                print(f"{'ID':<8} {'고객사명':<20} {'담당자':<12} {'이메일':<25}")
                print("-" * 65)
                for c in customers:
                    print(f"{c['customer_id']:<8} {c['customer_name']:<20} {c['manager_name']:<12} {c['email']:<25}")

        elif choice == '3':
            print_header("고객사 상세 조회")
            cid = input("고객 ID: ").strip().upper()
            from customer_service import detail
            c = detail(cid)
            if c:
                print(f"고객 ID    : {c['customer_id']}")
                print(f"고객사명   : {c['customer_name']}")
                print(f"담당자     : {c['manager_name']}")
                print(f"이메일     : {c['email']}")
            else:
                print("→ 존재하지 않는 고객사입니다.")

        elif choice == '4':
            print_header("고객사 검색")
            keyword = input("검색어 (고객사명/담당자명/이메일): ").strip()
            from customer_service import search
            results = search(keyword)
            if not results:
                print("검색 결과가 없습니다.")
            else:
                print(f"{'ID':<8} {'고객사명':<20} {'담당자':<12} {'이메일':<25}")
                print("-" * 65)
                for c in results:
                    print(f"{c['customer_id']:<8} {c['customer_name']:<20} {c['manager_name']:<12} {c['email']:<25}")

        elif choice == '5':
            print_header("고객사 수정")
            cid = input("고객 ID: ").strip().upper()
            from customer_service import detail, update
            c = detail(cid)
            if c is None:
                print("→ 존재하지 않는 고객사입니다.")
                continue
            print(f"현재 고객사명: {c['customer_name']}")
            new_name = input("새 고객사명 (변경 없으면 Enter): ").strip()
            print(f"현재 담당자: {c['manager_name']}")
            new_manager = input("새 담당자명 (변경 없으면 Enter): ").strip()
            print(f"현재 이메일: {c['email']}")
            new_email = input("새 이메일 (변경 없으면 Enter): ").strip()

            kwargs = {}
            if new_name:
                kwargs['customer_name'] = new_name
            if new_manager:
                kwargs['manager_name'] = new_manager
            if new_email:
                kwargs['email'] = new_email
            if not kwargs:
                print("→ 변경할 내용이 없습니다.")
                continue
            success, msg = update(cid, **kwargs)
            print(f"→ {msg}")

        elif choice == '6':
            print_header("고객사 삭제")
            cid = input("고객 ID: ").strip().upper()
            from customer_service import delete
            success, msg = delete(cid)
            print(f"→ {msg}")

        elif choice == '7':
            print_header("영업일지 등록")
            cid = input("고객 ID: ").strip().upper()
            date = input("활동 날짜 (YYYY-MM-DD): ").strip()
            content = input("영업 활동 내용: ").strip()
            from sales_report_service import register
            success, msg = register(cid, date, content)
            print(f"→ {msg}")

        elif choice == '8':
            print_header("영업일지 목록")
            from sales_report_service import list_all
            reports = list_all()
            if not reports:
                print("등록된 영업일지가 없습니다.")
            else:
                print(f"{'ID':<8} {'고객ID':<8} {'고객사명':<20} {'날짜':<12} {'상태':<12} {'내용':<30}")
                print("-" * 90)
                for r in reports:
                    content_preview = r['content'][:27] + '...' if len(r['content']) > 30 else r['content']
                    print(f"{r['report_id']:<8} {r['customer_id']:<8} {r.get('customer_name', '?'):<20} {r['activity_date']:<12} {r['status']:<12} {content_preview:<30}")

        elif choice == '9':
            print_header("영업일지 수정")
            rid = input("영업일지 ID: ").strip().upper()
            from sales_report_service import get_by_id, update
            r = get_by_id(rid)
            if r is None:
                print("→ 존재하지 않는 영업일지입니다.")
                continue
            print(f"현재 내용: {r['content']}")
            new_content = input("새 내용 (변경 없으면 Enter): ").strip()
            print(f"현재 날짜: {r['activity_date']}")
            new_date = input("새 날짜 (변경 없으면 Enter): ").strip()

            kwargs = {}
            if new_content:
                kwargs['content'] = new_content
            if new_date:
                kwargs['activity_date'] = new_date
            if not kwargs:
                print("→ 변경할 내용이 없습니다.")
                continue
            success, msg = update(rid, **kwargs)
            print(f"→ {msg}")

        elif choice == '10':
            print_header("영업일지 삭제")
            rid = input("영업일지 ID: ").strip().upper()
            from report_service import delete
            success, msg = delete(rid)
            print(f"→ {msg}")

        elif choice == '11':
            print_header("영업일지 상신")
            rid = input("영업일지 ID: ").strip().upper()
            from approval_service import submit
            success, msg = submit(rid)
            print(f"→ {msg}")

        elif choice == '12':
            print_header("영업일지 승인")
            rid = input("영업일지 ID: ").strip().upper()
            from approval_service import approve
            success, msg = approve(rid)
            print(f"→ {msg}")

        elif choice == '13':
            print_header("영업일지 반려")
            rid = input("영업일지 ID: ").strip().upper()
            from approval_service import reject
            success, msg = reject(rid)
            print(f"→ {msg}")

        elif choice == '14':
            print_header("영업일지 회수")
            rid = input("영업일지 ID: ").strip().upper()
            from approval_service import withdraw
            success, msg = withdraw(rid)
            print(f"→ {msg}")

        elif choice == '15':
            print_header("고객사별 활동 요약")
            cid = input("고객 ID: ").strip().upper()
            from summary_service import summarize_by_customer
            success, data = summarize_by_customer(cid)
            if not success:
                print(f"→ {data}")
            else:
                print(f"고객사명     : {data['customer_name']}")
                print(f"전체 보고서  : {data['total_reports']}건")
                print(f"승인 보고서  : {data['approved_reports']}건")
                if data['reports']:
                    print(f"\n{'ID':<8} {'날짜':<12} {'상태':<12} 내용")
                    print("-" * 60)
                    for r in data['reports']:
                        content_preview = r['content'][:27] + '...' if len(r['content']) > 30 else r['content']
                        print(f"{r['report_id']:<8} {r['activity_date']:<12} {r['status']:<12} {content_preview}")

        elif choice == '16':
            print_header("고객사 목록 CSV 내보내기")
            from csv_exporter import export_to_csv
            export_to_csv()

        else:
            print("→ 올바른 메뉴 번호를 입력하세요.")


if __name__ == '__main__':
    run()